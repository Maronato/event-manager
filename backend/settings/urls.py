from project.router import base_router
from . import api

base_router.register("settings", api.SettingsView, "settings")

apipatterns = []

app_name = "settings"
urlpatterns = []
