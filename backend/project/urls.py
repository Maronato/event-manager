from django.urls import path, include
from django.contrib import admin
from django.conf import settings
import debug_toolbar
from .authapi import ObtainJWT, VerifyJWT, RefreshJWT, LoginWithJWT, Logout
from .api import MeView
from .views import LoginView
admin.autodiscover()
# from app import views

jwt_auth_patterns = [
    path("login/", ObtainJWT.as_view(), name='login'),
    path("logout/", Logout.as_view(), name='logout'),
    path("login_with/", LoginWithJWT.as_view(), name='login_with'),
    path("verify/", VerifyJWT.as_view(), name='verify'),
    path("refresh/", RefreshJWT.as_view(), name='refresh'),
]

auth_patterns = [path("jwt/", include((jwt_auth_patterns, 'jwt'), namespace='jwt'))]

api_patterns = [
    path('me/', MeView.as_view(), name='me'),
]

urlpatterns = [
    path('api/', include((api_patterns, 'api'), namespace='api')),
    path("auth/", include((auth_patterns, 'auth'), namespace='auth')),
    path('', LoginView.as_view(), name='login'),
    path('', include('pwa.urls')),
    path('', include('django_prometheus.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('profile/', include('user_profile.urls')),
    path('social/', include('social.urls')),
    path('settings/', include('settings.urls')),
    path('application/', include('application.urls')),
    path('hacker/', include('hacker.urls')),
    path('staff/', include('staff.urls')),
    path('godmode/', include('godmode.urls')),
    path('company/', include('company.urls')),
    path('announcement/', include('announcement.urls')),
    path('stats/', include('stats.urls')),
    path('schedule/', include('schedule.urls')),
    path('helper/', include('helper.urls')),
    path('team/', include('team.urls')),
]


if settings.SHOW_TOOLBAR_CALLBACK:
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
