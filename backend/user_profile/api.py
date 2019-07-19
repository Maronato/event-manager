import time
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.db import connection
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import response, mixins, viewsets, serializers
from rest_framework_jwt.settings import api_settings
from godmode.permissions import IsAdmin
from staff.permissions import IsStaff
from settings.permissions import RegistrationOpen
from project.generics import PrefetchListAPIView
from .models import Profile, User
from .tasks import send_recover_token_email
from .serializers import (
    ListProfileSerializer,
    ListHackerProfileSerializer,
    SUIProfileListSerializer,
    TokenInputSerializer,
    EmailnputSerializer,
    CodenputSerializer
)


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class TokenLogin(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = TokenInputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        try:
            instance = Profile.objects.get(token=token)
            login(request, instance.user)
            return response.Response(
                {"token": jwt_encode_handler(jwt_payload_handler(instance.user))}
            )
        except Profile.DoesNotExist:
            time.sleep(2)
            return response.Response({"error": "Token inválido"}, status=404)


class CheckToken(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = TokenInputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        try:
            instance = Profile.objects.get(token=token)
            login(request, instance.user)
            return response.Response({"success": True})
        except Profile.DoesNotExist:
            time.sleep(2)
            return response.Response({"error": "Token inválido"}, status=404)


class ResetTokenEmail(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = EmailnputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.first()
            user.profile.new_token()
            send_recover_token_email.delay(user.profile.id)
        time.sleep(2)
        return response.Response({"message": "Olhe seu email :)"})


class ChangeEmail(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailnputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = request.user
        user.profile.change_email(email)
        time.sleep(2)
        return response.Response({"message": "Olhe seu email :)"})


class VerifyEmail(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [RegistrationOpen]
    permission_denied_message = "Estamos fora do período de registro"
    authentication_classes = []
    serializer_class = CodenputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        try:
            profile = Profile.objects.get(verification_code=code)
            profile.verify_email()
            login(request, profile.user)
            messages.success(request, "Email verificado")
            return response.Response({"message": "Email verificado", "token": jwt_encode_handler(jwt_payload_handler(profile.user))})
        except Profile.DoesNotExist:
            messages.error(request, "Código inválido")
            return response.Response({"error": "Código inválido"}, status=400)


class ChangeToken(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.Serializer

    def create(self, request):
        user = request.user
        token = user.profile.new_token()
        return response.Response({"message": "Token alterado", "token": token})


class ListProfiles(PrefetchListAPIView):
    serializer_class = ListProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAdmin]


class ListHackerProfiles(PrefetchListAPIView):
    serializer_class = ListHackerProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsStaff]

    def get_queryset(self):
        self.queryset = self.queryset.filter(
            shortcuts__state__in=[
                "checkedin",
                "confirmed",
                "waitlist",
                "admitted",
                "submitted",
                "declined",
            ]
        )
        return super().get_queryset()


class FrontendListProfiles(PrefetchListAPIView):
    serializer_class = SUIProfileListSerializer
    queryset = Profile.objects.filter(shortcuts__is_verified=True)
    permission_classes = [IsStaff]

    def get_queryset(self, *args, **kwargs):
        q = self.request.query_params.get("search", None)
        queryset = self.queryset
        if q:
            if connection.vendor == "postgresql":
                query = SearchQuery(q, config="portuguese")
                vectors = (
                    SearchVector(
                        "shortcuts__full_name", config="portuguese", weight="A"
                    )
                    + SearchVector("user__email", config="portuguese", weight="B")
                    + SearchVector("unique_id", config="portuguese", weight="C")
                )
                queryset = (
                    queryset.annotate(search=vectors)
                    .filter(
                        Q(shortcuts__full_name__icontains=q)
                        | Q(user__email__icontains=q)
                        | Q(unique_id__icontains=q)
                        | Q(search=query)
                    )
                    .annotate(rank=SearchRank(vectors, query))
                    .order_by("-rank")
                )
            else:
                queryset = queryset.filter(
                    Q(shortcuts__full_name__icontains=q)
                    | Q(user__email__icontains=q)
                    | Q(unique_id__icontains=q)
                )
        self.queryset = queryset
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(*args, **kwargs))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        success = True
        if len(serializer.data) == 0:
            success = False
        return response.Response({"success": success, "results": serializer.data})
