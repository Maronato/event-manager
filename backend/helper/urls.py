from project.router import base_router
from . import api

base_router.register("ticket", api.TicketViewset, "ticket")
base_router.register("mentor/me", api.SelfMentor, "mentor_self")
base_router.register("mentor/toggle", api.ToggleIsMentor, "mentor_toggle")
base_router.register("mentor", api.MentorViewset, "mentor")
base_router.register("online_mentors", api.OnlineMentorViewset, "online_mentors")

apipatterns = []

app_name = "helper"
urlpatterns = []
