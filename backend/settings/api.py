from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or, And
from project.permissions import IsReadyOnlyRequest
from godmode.permissions import IsAdmin
from .serializers import SettingsSerializer
from .models import Settings


class SettingsView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    single_instance_viewset = True
    serializer_class = SettingsSerializer
    permission_classes = [Or(IsAdmin, And(IsAuthenticated, IsReadyOnlyRequest))]

    def get_object(self):
        queryset = Settings.get()
        return queryset
