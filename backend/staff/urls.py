from project.router import base_router
from . import api


base_router.register('staff/toggle', api.ToggleIsStaff, 'staff_toggle')
base_router.register('hackers/create_blank', api.CreateBlankHacker, 'hacker_create_blank')

apipatterns = []

app_name = "staff"
urlpatterns = []
