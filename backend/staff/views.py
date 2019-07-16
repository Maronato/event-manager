from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin, PermissionClassesMixin
from .mixins import StaffContextMixin
from .permissions import IsStaff

# Create your views here.


class StaffView(
    PermissionClassesMixin,
    SidebarContextMixin,
    StaffContextMixin,
    UserContextMixin,
    TemplateView,
):
    template_name = "staff/staff.html"
    active_tab = "staff"
    permission_classes = [IsStaff]
