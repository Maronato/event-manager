from django.urls import path, include
from django.contrib import admin
from .views import LoginView
admin.autodiscover()
# from app import views

urlpatterns = [
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
