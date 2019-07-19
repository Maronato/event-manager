from project.router import base_router
from . import api


base_router.register("admin/toggle", api.ToggleIsAdmin, "admin_toggle")
base_router.register("users/delete", api.DeleteUser, "user_delete")
base_router.register("users/batch_create", api.BatchCreateUsers, "user_batch_create")

apipattens = []

app_name = "godmode"
urlpatterns = []
