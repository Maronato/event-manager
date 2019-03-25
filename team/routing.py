# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/subscriptions/team/<str:team_id>/<str:signal>/', consumers.TeamSignalConsumer, name='team_subscription'),
]
