from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin, PermissionClassesMixin
from rest_condition import Or
from godmode.permissions import IsAdmin
from staff.permissions import IsStaff
from company.permissions import EmployeeHasAccess
from .mixins import StatsContextMixin
# Create your views here.


class StatsView(
        PermissionClassesMixin,
        SidebarContextMixin,
        StatsContextMixin,
        UserContextMixin,
        TemplateView):
    template_name = 'stats/stats.html'
    active_tab = 'stats'

    permission_classes = [Or(IsAdmin, IsStaff, EmployeeHasAccess)]
