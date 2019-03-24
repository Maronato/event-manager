from django.views.generic import TemplateView
from .permissions import IsAdmin
from .mixins import AdminContextMixin
from project.mixins import SidebarContextMixin, UserContextMixin, PermissionClassesMixin
# Create your views here.


class AdminView(
        PermissionClassesMixin,
        SidebarContextMixin,
        AdminContextMixin,
        UserContextMixin,
        TemplateView):
    template_name = 'godmode/admin.html'
    active_tab = 'admin'
    permission_classes = [IsAdmin]
