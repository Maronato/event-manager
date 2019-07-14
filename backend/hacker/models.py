from django.db.models.signals import post_save, pre_delete
from django.db import models
from django.utils import timezone
from pagseguro.signals import notificacao_recebida
from pagseguro.api import PagSeguroApi
from user_profile.models import Profile
from settings.models import Settings
from team.models import Team
from . import tasks
# Create your models here.


class Hacker(models.Model):

    # Subscription fields
    msocks_allow = True
    msocks_serializer = 'hacker.serializers.HackerSubscriptionSerializer'

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )

    # Admitted by an admin
    admitted = models.BooleanField(default=False)
    # Declined by an admin
    declined = models.BooleanField(default=False)
    # Admitted but put on waitlist
    waitlist = models.BooleanField(default=False)
    # Datetime of waitlist (so that when the waitlist is refreshed, hackers are
    # admitted in order)
    waitlist_date = models.DateTimeField(null=True, blank=True)
    # Admitted but gave up
    withdraw = models.BooleanField(default=False)
    # Admitted and confirmed that can attend
    confirmed = models.BooleanField(default=False)
    # Checked in at the event
    checked_in = models.BooleanField(default=False)

    # Payment status
    # Internal payment transaction referece
    transaction_reference = models.CharField(max_length=32, default='', blank=True)

    # Team
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name='hackers',
        null=True
    )

    @property
    def payed(self):
        return self.transactions.filter(status__in=['pago', 'disponivel']).filter(reference=self.transaction_reference).exists()

    @property
    def transaction_status(self):
        return self.transactions.get(reference=self.transaction_reference).get_status_display() if self.transactions.filter(reference=self.transaction_reference).exists() else 'Não pago'

    @property
    def hacker_state(self):
        # If the user submitted an application but didn't pay (i.e. asked for a refund or something)
        if Settings.get().require_payment and not self.payed and hasattr(self, 'application'):
            return 'unpaid'
        if self.checked_in:
            return 'checkedin'
        if self.confirmed:
            return "confirmed"
        if not Settings.can_confirm(self.waitlist):
            return "late"
        if self.withdraw:
            return "withdraw"
        if self.waitlist:
            return "waitlist"
        if self.admitted:
            return "admitted"
        if self.declined:
            return "declined"
        if hasattr(self, 'application'):
            return "submitted"
        if not Settings.registration_is_open():
            return "late"
        return "incomplete"

    def admit(self, send_email=True):
        # Admit hacker and send notification email
        # Also called when a hacker that has withdrowned changes their mind
        self.admitted = True
        self.declined = False
        self.waitlist = False
        self.withdraw = False
        self.save()

        if Settings.is_full():
            # If event is full
            return self.put_on_waitlist(send_email)
        if send_email:
            tasks.send_notify_admitted.delay(self.id)

    def nag_admitted(self):
        # Remember hacker that they've been admitted
        tasks.send_nag_admitted.delay(self.id)

    def decline(self):
        self.admitted = False
        self.confirmed = False
        self.declined = True
        self.waitlist = False
        self.withdraw = False
        self.save()
        tasks.send_notify_decline.delay(self.id)
        Hacker.cycle_waitlist()

        for transaction in self.transactions.filter(status__in=['pago', 'disponivel']):
            PagSeguroApi().refund_transaction(transaction.code)

    def put_on_waitlist(self, send_email=True):
        # Put hacker on waitlist (Done automatically by the server
        # if the event is full)
        self.waitlist = True
        self.waitlist_date = timezone.now()
        self.save()
        if send_email:
            tasks.send_notify_waitlist.delay(self.id)

    def unwaitlist(self, force=False):
        # Remove hacker from waitlist
        if not force:
            self.admit(False)
        else:
            # This ignores the maximum number of hackers allowed
            self.waitlist = False
            self.save()
        tasks.send_notify_unwaitlist.delay(self.id)

    def withdraw_from_event(self):
        # Withdraw hacker from event
        self.confirmed = False
        self.withdraw = True
        self.admitted = False
        self.save()
        Hacker.cycle_waitlist()

        for transaction in self.transactions.filter(status__in=['pago', 'disponivel']):
            PagSeguroApi().refund_transaction(transaction.code)

    def confirm(self):
        # Hacker confirmed presence
        self.confirmed = True
        self.save()

    def check_in(self):
        self.checked_in = True
        self.save()

    @classmethod
    def cycle_waitlist(cls):
        # get the current waitlist
        waitlist = list(cls.objects.filter(waitlist=True).order_by('waitlist_date'))
        # while the event is not full and there are waitlisted hackers
        while not Settings.is_full() and len(waitlist) > 0:
            hacker = waitlist.pop(0)
            # Hacker can be waitlisted but not in waitlist(e.g late)
            if hacker.profile.state == 'waitlist':
                hacker.unwaitlist()

    @classmethod
    def handle_payment_notification(cls, sender, transaction, **kwargs):
        from pagseguro.models import Transaction
        reference = transaction['reference']
        hacker = cls.objects.filter(transaction_reference=reference)
        trans = Transaction.objects.filter(reference=reference)
        if hacker.exists() and trans.exists():
            hacker = hacker.first()
            trans = trans.first()
            hacker.transactions.add(trans)
            if transaction['status'] not in ['3', '4']:
                hacker.checked_in = False
                hacker.confirmed = False
                hacker.save()
                cls.cycle_waitlist()
            hacker.profile.trigger_update()

    def __str__(self):
        return f'Hacker {self.profile}'


def update_hacker(sender, **kwargs):
    # Updates profile
    kwargs['instance'].profile.trigger_update()


def delete_hacker(sender, **kwargs):
    profile = kwargs['instance'].profile
    profile.hacker = None
    profile.trigger_update()
    profile.hacker = kwargs['instance']


post_save.connect(update_hacker, sender=Hacker)
pre_delete.connect(delete_hacker, sender=Hacker)
notificacao_recebida.connect(Hacker.handle_payment_notification)
