from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from rest_condition import Or, And
from project.mixins import SidebarContextMixin, UserContextMixin, PermissionClassesMixin
from hacker.permissions import IsSubmitted, IsIncomplete, IsHacker
from user_profile.permissions import IsVerified
from settings.permissions import RegistrationOpen
from .forms import ApplicationForm

# Create your views here.


class ApplicationView(
    PermissionClassesMixin, SidebarContextMixin, UserContextMixin, FormView
):
    template_name = "application/application.html"
    form_class = ApplicationForm
    active_tab = "application"
    permission_classes = [
        And(Or(IsSubmitted, IsIncomplete, And(IsHacker, IsVerified)), RegistrationOpen)
    ]

    def form_valid(self, form):
        form.save(hacker=self.request.user.profile.hacker)
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Aplicação enviada!")
        return reverse_lazy("dashboard:index")

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        hacker = self.request.user.profile.hacker
        kwargs["instance"] = getattr(hacker, "application", None)
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["first_name"] = self.request.user.first_name
        initial["last_name"] = self.request.user.last_name
        initial["email"] = self.request.user.email
        return initial
