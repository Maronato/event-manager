from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework import viewsets, mixins, response, serializers
from project.serializers import UniqueIDSerializer
from user_profile.models import Profile
from user_profile.tasks import send_verify_email
from .permissions import IsAdmin
from .serializers import BatchUserSerializer


def generate_dummy_data(count):
    data = {
        "send_emails": False,
        "users": [
            {"first_name": "temp", "last_name": str(i), "email": f"temp{i}@email.com"}
            for i in range(count)
        ],
    }
    return data


class ToggleIsAdmin(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdmin]
    serializer_class = UniqueIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unique_id = serializer.validated_data["unique_id"]
        user = Profile.objects.get(unique_id=unique_id).user
        user.is_superuser = not user.is_superuser
        user.save()
        return response.Response({"message": "Permissão alterada"})


class DeleteUser(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    lookup_field = "profile__unique_id"
    lookup_url_kwarg = "unique_id"


class BatchCreateUsers(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdmin]
    serializer_class = BatchUserSerializer

    def uniqueUsername(self):
        username = get_random_string(length=30)
        # if User.objects.filter(username=username).exists():
        #     return self.uniqueUsername()
        return username

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        users = serializer.validated_data["users"]
        send_emails = serializer.validated_data["send_emails"]

        # Make sure emails are unique
        if len(users) != len(set(map(lambda x: x["email"], users))):
            raise serializers.ValidationError(
                "Existem usuários com emails repetidos na lista"
            )

        # Generate a map to search faster
        user_map = {user["email"]: user for user in users}

        # all user emails
        all_user_emails = {user["email"] for user in users}

        # Find which users already exist
        existing_user_emails = set(
            User.objects.filter(email__in=user_map.keys()).values_list(
                "email", flat=True
            )
        )

        # Flag errored users
        for email in existing_user_emails:
            user_map[email]["result"] = "error"

        new_user_emails = all_user_emails.difference(existing_user_emails)

        # Bulk create users
        to_create_users = list(
            map(
                lambda email: User(username=self.uniqueUsername(), **user_map[email]),
                new_user_emails,
            )
        )
        User.objects.bulk_create(to_create_users)
        created_users = User.objects.filter(email__in=new_user_emails)

        # Flag success users
        for user in created_users:
            user_map[user.email]["result"] = "success"
            # Send signal that creates profiles
            post_save.send(User, instance=user, created=True)

        # Ge thte created profiles
        created_profiles = Profile.objects.filter(
            user__in=created_users
        ).select_related("user")

        # Batch update profiles
        created_profiles.update(verified=True)

        for profile in created_profiles:
            # Add token info
            user_map[profile.user.email]["token"] = profile.token
            # Send signal that creates profiles
            post_save.send(Profile, instance=profile, created=False)
            if send_emails:
                send_verify_email.delay(profile.id)

        return response.Response({"users": users})
