from django.views.generic import RedirectView
from django.conf import settings
from django.contrib.messages import add_message, ERROR
from django.utils.crypto import get_random_string
from pagseguro.api import PagSeguroItem, PagSeguroApi
from settings.mixins import CanConfirmMixin
from settings.models import Settings

# Create your views here.


class PaymentView(
        CanConfirmMixin,
        RedirectView):

    http_method_names = ['get']
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        sett = Settings.get()
        if not sett.require_payment:
            add_message(self.request, ERROR, 'Pagamentos desabilitados')
            return '/'
        item = PagSeguroItem(
            id='1',
            description=f'Ingresso para {settings.EVENT_NAME}',
            amount=f'{sett.ticket_price}',
            quantity=1
        )
        reference = get_random_string(length=32)
        api = PagSeguroApi(reference=reference)
        api.add_item(item)
        checkout = api.checkout()
        if checkout['success']:
            print(checkout)
            hacker = self.request.user.profile.hacker
            hacker.transaction_reference = reference
            hacker.save()
            return checkout['redirect_url']
        else:
            add_message(self.request, ERROR, 'Erro ao criar pedido de pagamento')
            return '/'
