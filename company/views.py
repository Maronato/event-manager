from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin, PermissionClassesMixin
from .permissions import EmployeeHasAccess
from .mixins import CompanyContextMixin
# Create your views here.


class CompanyView(
        PermissionClassesMixin,
        SidebarContextMixin,
        CompanyContextMixin,
        UserContextMixin,
        TemplateView):
    template_name = 'company/company.html'
    active_tab = 'company'
    permission_classes = [
        EmployeeHasAccess
    ]
    access_level = 0
