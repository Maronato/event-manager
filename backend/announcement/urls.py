from django.urls import path, include
from project.router import base_router
from . import api

base_router.register("announcement", api.AnnouncementViewset, "announcement")

apipatterns = []

app_name = "announcement"
urlpatterns = []
