from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.crypto import get_random_string
from rest_framework import views, mixins, viewsets, serializers
from project.serializers import UniqueIDSerializer
from godmode.permissions import IsAdmin
from user_profile.models import Profile
from hacker.models import Hacker
from .permissions import IsStaff
from .models import Staff


class ToggleIsStaff(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdmin]
    serializer_class = UniqueIDSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_id = serializer.validated_data["unique_id"]
        profile = Profile.objects.get(unique_id=unique_id)
        if profile.is_staff:
            profile.staff.delete()
            profile.trigger_update()
        else:
            staff = Staff(profile=profile)
            staff.save()
        return views.Response({"message": "Permissão alterada"})


class CreateBlankHacker(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsStaff]
    serializer_class = serializers.Serializer

    def uniqueUsername(self):
        username = get_random_string(length=20)
        if User.objects.filter(username=username).exists():
            return self.uniqueUsername()
        return username

    def post(self, request):
        user = User(username=self.uniqueUsername())
        user.save()
        hacker = Hacker(profile=user.profile)
        hacker.save()
        return views.Response({"token": user.profile.token})
