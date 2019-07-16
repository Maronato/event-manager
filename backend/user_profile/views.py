from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.messages import add_message, ERROR, SUCCESS
from django.contrib.auth import login
from project.mixins import PermissionClassesMixin
from settings.permissions import RegistrationOpen
from .models import Profile
# Create your views here.


class VerifyEmailView(
        PermissionClassesMixin,
        View):

    http_method_names = ['get']
    permission_classes = [RegistrationOpen]
    permission_denied_message = 'Estamos fora do período de registro'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code', 'invalid')
        try:
            profile = Profile.objects.get(verification_code=code)
            add_message(request, SUCCESS, 'Email verificado')
            profile.verify_email()
            login(request, profile.user)
        except Profile.DoesNotExist:
            add_message(request, ERROR, 'Código inválido')

        return redirect('dashboard:index')
