from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from project.mixins import SidebarContextMixin, UserContextMixin, PermissionClassesMixin
from .mixins import DashboardContextMixin


class Dashboard(
        PermissionClassesMixin,
        SidebarContextMixin,
        DashboardContextMixin,
        UserContextMixin,
        TemplateView):

    template_name = 'dashboard/dashboard.html'
    active_tab = 'dashboard'
    permission_classes = [IsAuthenticated]
