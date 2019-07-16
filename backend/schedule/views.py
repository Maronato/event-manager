from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin, PermissionClassesMixin
from .mixins import ScheduleContextMixin
from .permissions import CanAttendEvents

# Create your views here.


class ScheduleView(
    PermissionClassesMixin,
    SidebarContextMixin,
    ScheduleContextMixin,
    UserContextMixin,
    TemplateView,
):
    template_name = "schedule/schedule.html"
    active_tab = "schedule"
    permission_classes = [CanAttendEvents]
