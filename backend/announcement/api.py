from rest_framework import viewsets
from project.mixins import PrefetchQuerysetModelMixin
from .permissions import can_see_announcements
from .serializers import AnnouncementSerializer
from .models import Announcement


class AnnouncementViewset(PrefetchQuerysetModelMixin, viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = can_see_announcements
    queryset = Announcement.objects.all().order_by("-created")
