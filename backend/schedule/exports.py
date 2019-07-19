from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from project.mixins import ExportMixin, PrefetchQuerysetModelMixin
from godmode.permissions import IsAdmin
from .permissions import CanAttendEvents
from .models import Event, Feedback
from .export_serializers import ExportFeedbackSerializer, ExportEventSerializer


class ExportEventsViewset(
    ExportMixin, PrefetchQuerysetModelMixin, ReadOnlyModelViewSet
):
    serializer_class = ExportEventSerializer
    queryset = Event.objects.all()

    @property
    def permission_classes(self):
        if self.action == "feedback":
            return [CanAttendEvents]
        return [IsAdmin]

    def get_queryset(self):
        if self.action == "feedback":
            event = self.get_object()
            if event.speaker != self.request.user.profile:
                return Feedback.objects.none()
            return event.feedbacks.all()
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "feedback":
            return ExportFeedbackSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["get"])
    def feedback(self, request, pk=None):
        return super().list(self, request)
