from project.router import base_router
from . import api

base_router.register("teams", api.TeamViewset)

apipatterns = []

app_name = "team"
urlpatterns = []
