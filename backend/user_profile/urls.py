from rest_framework.routers import DefaultRouter
from project.router import base_router
from . import api

auth_router = DefaultRouter()

auth_router.register('check', api.CheckToken, 'check')
auth_router.register('login', api.TokenLogin, 'login')

tokenauthpatterns = auth_router.urls

base_router.register('profile/change_email', api.ChangeEmail, 'profile_change_email')
base_router.register('profile/verify_email', api.VerifyEmail, 'profile_verify_email')
base_router.register('profile/change_token', api.ChangeToken, 'profile_change_token')
base_router.register('profile/reset_token_email', api.ChangeEmail, 'profile_reset_token_email')
base_router.register('profile/all', api.ListProfiles, 'profile_list_all')
base_router.register('profile/all_frontend', api.FrontendListProfiles, 'profile_list_all_frontend')
base_router.register('profile/hackers', api.ListHackerProfiles, 'profile_list_hackers')

apipattens = []

app_name = "profile"
urlpatterns = []