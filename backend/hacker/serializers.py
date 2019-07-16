from rest_framework import serializers
from project.mixins import SingleInstancePrefetchMixin
from .models import Hacker


class HackerSubscriptionSerializer(
    SingleInstancePrefetchMixin, serializers.ModelSerializer
):

    unique_id = serializers.CharField(source="profile.unique_id")
    email = serializers.CharField(source="profile.user.email")
    full_name = serializers.CharField(source="profile.shortcuts.full_name")
    state = serializers.CharField(source="profile.shortcuts.state")

    class Meta:
        model = Hacker
        fields = ["unique_id", "email", "full_name", "state", "transaction_status"]
        select_related_fields = ["profile", "profile__shortcuts"]
        prefetch_related_fields = ["transactions"]
