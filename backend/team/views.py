from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin, PermissionClassesMixin
from hacker.permissions import IsCheckedin
from .mixins import TeamContextMixin

# Create your views here.


class TeamView(
    PermissionClassesMixin,
    SidebarContextMixin,
    TeamContextMixin,
    UserContextMixin,
    TemplateView,
):
    template_name = "team/team.html"
    active_tab = "team"
    permission_classes = [IsCheckedin]
