from django.shortcuts import reverse
from django.views.generic.base import ContextMixin
from .models import Settings
import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


class SettingsContextMixin(ContextMixin):
    """Settings Context

    Inherit this mixin to automatically get the event settings
    """

    def get_context_data(self, **kwargs):
        settings = Settings.get()
        settings_context = {
            'max_hackers': settings.max_hackers,
            'default_hacker': Settings.default_hacker(settings=settings),
            'default_staff': Settings.default_staff(settings=settings),
            'auto_admit_hackers': Settings.auto_admit_hackers(settings=settings),
            'verify_email': settings.verify_email,
            'registration_opened': Settings.registration_opened(settings=settings),
            'registration_is_open': Settings.registration_is_open(settings=settings),
            'can_confirm': Settings.can_confirm(settings=settings),
            'is_full': Settings.is_full(settings=settings),
            'hackathon_is_happening': Settings.hackathon_is_happening(settings=settings),
            'hackathon_ended': Settings.hackathon_ended(settings=settings),
            'registration_open_seconds': Settings.registration_open_seconds(settings=settings),
            'registration_close_seconds': Settings.registration_close_seconds(settings=settings),
            'confirmation_seconds': Settings.confirmation_seconds(settings=settings),
            'hackathon_start_seconds': Settings.hackathon_start_seconds(settings=settings),
            'hackathon_end_seconds': Settings.hackathon_end_seconds(settings=settings),
            'ticket_expire': settings.ticket_expire,
            'ticket_queue_open': settings.ticket_queue_open,
            'ticket_price': settings.ticket_price,
            'require_payment': settings.require_payment,
            'api': {
                'dashboard': reverse('dashboard:index'),
            }
        }
        context = super().get_context_data(**kwargs)
        context['settings_context'] = json.dumps(settings_context, cls=DecimalEncoder)
        return context
