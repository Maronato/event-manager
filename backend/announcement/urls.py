from django.urls import path, include
from project.router import base_router
from . import api

base_router.register("announcements", api.AnnouncementViewset, "announcement")

apipatterns = []

app_name = "announcement"
urlpatterns = []
