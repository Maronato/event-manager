from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from announcement.urls import urlpatterns as announcement_urls
from application.urls import urlpatterns as application_urls
from company.urls import urlpatterns as company_urls
from godmode.urls import urlpatterns as godmode_urls
from hacker.urls import urlpatterns as hacker_urls
from hacker.urls import payment_urlpatterns as payment_urls
from helper.urls import urlpatterns as helper_urls
from user_profile.urls import tokenauthpatterns as token_auth_patterns
from .router import base_router, export_router
from .authapi import ObtainJWT, VerifyJWT, RefreshJWT, LoginWithJWT, Logout
from .api import MeView

admin.autodiscover()
# from app import views

jwt_auth_patterns = [
    path("login/", ObtainJWT.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("login_with/", LoginWithJWT.as_view(), name="login_with"),
    path("verify/", VerifyJWT.as_view(), name="verify"),
    path("refresh/", RefreshJWT.as_view(), name="refresh"),
]

auth_patterns = [
    path("jwt/", include((jwt_auth_patterns, "jwt"), namespace="jwt")),
    path("token/", include((token_auth_patterns, "token"), namespace="token"))
]

api_patterns = base_router.urls
export_patterns = export_router.urls

api_patterns += [
    path("me/", MeView.as_view(), name="me")
]

urlpatterns = [
    path("api/", include((api_patterns, "api"), namespace="api")),
    path("export/", include((export_patterns, "export"), namespace="export")),
    path("auth/", include((auth_patterns, "auth"), namespace="auth")),
    path("payment/", include((payment_urls, "payment"), namespace="payment")),
    path("", include("django_prometheus.urls")),
    path("admin/", admin.site.urls),
]


if settings.SHOW_TOOLBAR_CALLBACK:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
