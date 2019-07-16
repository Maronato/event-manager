# from django.urls import path, include
from project.router import base_router
from . import api


base_router.register("company", api.CompanyViewset, "company")
base_router.register("employee", api.EmployeeViewset, "employee")
base_router.register("scan/hacker/fetch", api.FetchScanHacker, "scan_hacker_fetch")
base_router.register("scan/hacker", api.ScanHacker, "scan_hacker")
base_router.register("scan/employee/fetch", api.FetchCheckinEmployee, "scan_employee_fetch")
base_router.register("scan/employee", api.CheckinEmployee, "scan_employee")
base_router.register("scan", api.ScanViewset, "scan")

apipatterns = [
]

app_name = "company"
urlpatterns = [
]
