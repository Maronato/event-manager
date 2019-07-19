from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, mixins, response
from rest_condition import Or, And
from settings.permissions import CanConfirm
from godmode.permissions import IsAdmin
from project.serializers import UniqueIDSerializer
from staff.permissions import IsStaff
from user_profile.models import Profile
from .permissions import IsAdmitted, IsWithdraw, IsConfirmed
from .models import Hacker


class ConfirmPresence(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [And(IsAdmitted, CanConfirm)]

    def create(self, request):
        hacker = request.user.profile.hacker
        hacker.confirm()
        return response.Response(
            {"message": "Presença confirmada", "state": hacker.profile.state}
        )


class Withdraw(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [Or(IsAdmitted, IsConfirmed)]

    def create(self, request):
        hacker = request.user.profile.hacker
        hacker.withdraw_from_event()
        return response.Response(
            {"message": "Desistência completa", "state": hacker.profile.state}
        )


class UndoWithdraw(mixins.CreateModelMixin, viewsets.GenericViewSet):

    permission_classes = [And(IsWithdraw, CanConfirm)]

    def create(self, request):
        hacker = request.user.profile.hacker
        hacker.admit(False)
        return response.Response(
            {"message": "Desistência desfeita", "state": hacker.profile.state}
        )


class Admit(mixins.CreateModelMixin, viewsets.GenericViewSet):

    permission_classes = [IsStaff]
    serializer_class = UniqueIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_id = serializer.validated_data["unique_id"]
        hacker = get_object_or_404(Hacker, profile__unique_id=unique_id)
        if hacker.profile.state not in ["submitted", "declined"]:
            return response.Response(
                {"message": "State is not submitted or declined"}, status=400
            )
        hacker.admit()
        return response.Response({"message": "Hacker admitido"})


class Decline(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsStaff]
    serializer_class = UniqueIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_id = serializer.validated_data["unique_id"]
        hacker = get_object_or_404(Hacker, profile__unique_id=unique_id)
        if hacker.profile.state not in ["submitted", "admitted", "confirmed"]:
            return response.Response(
                {"message": "State is not in 'submitted', 'admitted', 'confirmed'"},
                status=400,
            )
        hacker.decline()
        return response.Response({"message": "Hacker rejeitado"})


class Unwaitlist(mixins.CreateModelMixin, viewsets.GenericViewSet):

    permission_classes = [IsStaff]
    serializer_class = UniqueIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_id = serializer.validated_data["unique_id"]
        hacker = get_object_or_404(Hacker, profile__unique_id=unique_id)
        if hacker.profile.state != "waitlist":
            return response.Response({"message": "State is not waitlist"}, status=400)
        hacker.unwaitlist(True)
        return response.Response({"message": "Hacker tirado da fila"})


class ToggleIsHacker(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdmin]
    serializer_class = UniqueIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_id = serializer.validated_data["unique_id"]
        profile = Profile.objects.get(unique_id=unique_id)
        if profile.is_hacker:
            profile.hacker.delete()
        else:
            hacker = Hacker(profile=profile)
            hacker.save()
        return response.Response({"message": "Permissão alterada"})


class FetchCheckinHacker(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsStaff]
    serializer_class = UniqueIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_id = serializer.validated_data["unique_id"]
        try:
            profile = Profile.objects.get(
                Q(unique_id=unique_id) | Q(user__email=unique_id)
            )
        except Profile.DoesNotExist:
            return response.Response(
                {
                    "title": "Usuário não existe!",
                    "message": "Não foi possível encontrar um usuário válido com esse código",
                    "status": "error",
                }
            )
        if not profile.is_hacker:
            return response.Response(
                {
                    "title": "Usuário não é hacker!",
                    "message": "Esse usuário é válido, mas não é um hacker",
                    "status": "error",
                }
            )
        if profile.state == "checkedin":
            return response.Response(
                {
                    "title": "Hacker já fez Check-In!",
                    "message": "Hackers só podem fazer check-in uma vez",
                    "status": "error",
                }
            )
        if profile.state != "confirmed":
            return response.Response(
                {
                    "title": "Hacker não está confirmado!",
                    "message": "Apenas hackers que confirmaram presença podem fazer check-in",
                    "status": "error",
                }
            )

        return response.Response(
            {
                "title": f"{profile.full_name}",
                "message": f"Deseja fazer o check-in de {profile.full_name}?",
                "status": "success",
            }
        )


class CheckinHacker(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsStaff]
    serializer_class = UniqueIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_id = serializer.validated_data["unique_id"]
        profile = get_object_or_404(
            Profile, Q(unique_id=unique_id) | Q(user__email=unique_id)
        )
        if not profile.state == "confirmed":
            return response.Response({"error": "Invalid hacker ID"}, status=400)
        hacker = profile.hacker
        hacker.check_in()
        return response.Response({"message": "Check-In complete"})
