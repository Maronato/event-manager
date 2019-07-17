from project.router import base_router
from . import api

base_router.register("tickets", api.TicketViewset, "ticket")
base_router.register("mentors/me", api.SelfMentor, "mentor_self")
base_router.register("mentors/toggle", api.ToggleIsMentor, "mentor_toggle")
base_router.register("mentors/online", api.OnlineMentorViewset, "online_mentors")
base_router.register("mentors", api.MentorViewset, "mentor")

apipatterns = []

app_name = "helper"
urlpatterns = []
