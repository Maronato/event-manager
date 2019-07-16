from django.views.generic import TemplateView
from rest_condition import Or
from project.mixins import SidebarContextMixin, UserContextMixin, PermissionClassesMixin
from .mixins import HelperContextMixin
from .permissions import CanSubmitTickets, IsMentor

# Create your views here.


class HelperView(
    PermissionClassesMixin,
    SidebarContextMixin,
    HelperContextMixin,
    UserContextMixin,
    TemplateView,
):
    template_name = "helper/helper.html"
    active_tab = "helper"
    permission_classes = [Or(IsMentor, CanSubmitTickets)]
