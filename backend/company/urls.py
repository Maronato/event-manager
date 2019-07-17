# from django.urls import path, include
from project.router import base_router
from . import api


base_router.register("companies", api.CompanyViewset, "company")
base_router.register("employees", api.EmployeeViewset, "employee")
base_router.register("scans/hacker/fetch", api.FetchScanHacker, "scan_hacker_fetch")
base_router.register("scans/hacker", api.ScanHacker, "scan_hacker")
base_router.register("scans/employee/fetch", api.FetchCheckinEmployee, "scan_employee_fetch")
base_router.register("scans/employee", api.CheckinEmployee, "scan_employee")
base_router.register("scans", api.ScanViewset, "scan")

apipatterns = [
]

app_name = "company"
urlpatterns = [
]
