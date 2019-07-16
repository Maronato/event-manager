# from django.urls import path, include
from project.router import base_router
from . import api


base_router.register('staff/view_application', api.ViewHackerApplication, 'view_application')
base_router.register('hacker/application/form_options', api.FormOptions, 'form_options')
base_router.register('hacker/application', api.ApplicationViewset, 'application')

app_name = "application"
urlpatterns = [
]
