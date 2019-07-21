from django.urls import path
from project.router import base_router
from . import views, api


base_router.register('social/unlink', api.UnlinkProvider, "social_unlink")

apipattens = []

app_name = "social"

urlpatterns = [
    path("login/<str:provider>/", views.SocialLogin.as_view(), name="login"),
    path(
        "login_response/<str:provider>/",
        views.SocialLoginResponse.as_view(),
        name="login_response",
    ),
]
