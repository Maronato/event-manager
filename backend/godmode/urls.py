from project.router import base_router
from . import views, api


base_router.register('admin/toggle', api.ToggleIsAdmin, 'admin_toggle')
base_router.register('user/delete', api.DeleteUser, 'user_delete')
base_router.register('user/batch_create', api.BatchCreateUsers, 'user_batch_create')

apipattens = []

app_name = "godmode"
urlpatterns = []
