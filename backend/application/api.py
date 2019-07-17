from rest_framework import viewsets, mixins, response, permissions
from rest_condition import Or, And
from project.mixins import PrefetchQuerysetModelMixin
from hacker.permissions import IsSubmitted, IsIncomplete, IsHacker
from user_profile.permissions import IsVerified
from settings.permissions import RegistrationOpen
from staff.permissions import IsStaff
from .serializers import (
    ApplicationRetrieveSerializer,
    FormOptionsSerializer,
    FormOptionChoicesSerializer,
    ApplicationSerializer,
    get_form_option_choices,
)
from .models import Application


class ViewHackerApplication(
        PrefetchQuerysetModelMixin,
        viewsets.ReadOnlyModelViewSet):
    serializer_class = ApplicationRetrieveSerializer
    permission_classes = [IsStaff]
    queryset = Application.objects.all()
    lookup_field = "hacker__profile__unique_id"
    lookup_url_kwarg = "unique_id"


class FormOptions(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FormOptionChoicesSerializer
    queryset = []

    def get_data_list(self, option):
        self.retrieve
        import csv

        with open(f"application/choices/{option}.csv") as f:
            return {
                "results": [
                    {k: v for k, v in row.items()}
                    for row in csv.DictReader(f, skipinitialspace=True)
                ]
            }

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=list(map(lambda x: {"option": x}, get_form_option_choices())), many=True
        )
        serializer.is_valid()
        return response.Response(serializer.validated_data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={"option": self.kwargs.get("pk", False)})
        serializer.is_valid(raise_exception=True)
        option = serializer.validated_data["option"]
        try:
            data = self.get_data_list(option)
            serializer = FormOptionsSerializer(data=data)
            if serializer.is_valid():
                return response.Response(serializer.validated_data)
        except FileNotFoundError:
            pass
        serializer = FormOptionsSerializer(data={"success": False, "results": []})
        serializer.is_valid()
        return response.Response(serializer.validated_data)


class ApplicationViewset(
    PrefetchQuerysetModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    single_instance_viewset = True
    permission_classes = [
        And(Or(IsSubmitted, IsIncomplete, And(IsHacker, IsVerified)), RegistrationOpen)
    ]
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["hacker"] = self.request.user.profile.hacker
        return context

    def get_object(self):
        hacker = self.request.user.profile.hacker
        return getattr(hacker, "application", None)
