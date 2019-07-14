from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api

router = DefaultRouter()
router.register(r'team', api.TeamViewset)

apipatterns = router.urls

app_name = 'team'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api'),
    path('', views.TeamView.as_view(), name='index'),
]
