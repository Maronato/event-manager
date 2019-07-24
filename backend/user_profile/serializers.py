from rest_framework import serializers
from django.db.models.functions import Concat
from django.db.models import CharField, Value
from project.mixins import PrefetchMixin, SingleInstancePrefetchMixin
from .models import Profile


class SimpleProfileSerializer(PrefetchMixin, serializers.ModelSerializer):

    full_name = serializers.CharField(source="shortcuts.full_name")
    email = serializers.EmailField(source="user.email")
    state = serializers.CharField(source="shortcuts.state")

    class Meta:
        model = Profile
        fields = ["unique_id", "full_name", "email", "state"]
        select_related_fields = ["shortcuts", "user"]


class ListProfileSerializer(PrefetchMixin, serializers.ModelSerializer):
    has_facebook = serializers.BooleanField(source="shortcuts.has_facebook", required=False)
    has_github = serializers.BooleanField(source="shortcuts.has_github", required=False)
    has_google = serializers.BooleanField(source="shortcuts.has_google", required=False)

    # Belonging attributes
    is_hacker = serializers.BooleanField(source="shortcuts.is_hacker", required=False)
    is_staff = serializers.BooleanField(source="shortcuts.is_staff", required=False)
    is_employee = serializers.BooleanField(source="shortcuts.is_employee", required=False)
    is_admin = serializers.BooleanField(source="shortcuts.is_admin", required=False)
    is_mentor = serializers.BooleanField(source="shortcuts.is_mentor", required=False)

    # Control attributes
    state = serializers.CharField(source="shortcuts.state", required=False)
    is_verified = serializers.BooleanField(source="shortcuts.is_verified", required=False)

    full_name = serializers.CharField(source="shortcuts.full_name", required=False)

    payment_state = serializers.CharField(source="shortcuts.payment_state", required=False)

    class Meta:
        model = Profile
        fields = [
            "unique_id",
            "full_name",
            "email",
            "state",
            "is_verified",
            "is_hacker",
            "is_staff",
            "is_admin",
            "is_employee",
            "is_mentor",
            "employee_company_access",
            "has_facebook",
            "has_github",
            "has_google",
            "payment_state",
        ]
        select_related_fields = ["shortcuts", "user", "employee__company"]


class ListHackerProfileSerializer(SimpleProfileSerializer):
    pass


class SUIProfileListSerializer(PrefetchMixin, serializers.ModelSerializer):

    name = serializers.CharField()
    value = serializers.EmailField(source="unique_id")

    def setup_eager_loading(self, queryset):
        meta = self.Meta
        if hasattr(meta, "select_related_fields"):
            queryset = queryset.select_related(*meta.select_related_fields)
        if hasattr(meta, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*meta.prefetch_related_fields)

        queryset = queryset.annotate(
            name=Concat(
                "shortcuts__full_name",
                Value(" ("),
                "user__email",
                Value(")"),
                output_field=CharField(),
            )
        )
        return queryset

    class Meta:
        model = Profile
        fields = ["name", "value"]
        select_related_fields = ["shortcuts", "user"]


class UserSubscriptionSerializer(SingleInstancePrefetchMixin, ListProfileSerializer):
    """Allow Single instance prefetching"""


class SelfSubscriptionSerializer(UserSubscriptionSerializer):
    class Meta(UserSubscriptionSerializer.Meta):
        fields = ["token"] + UserSubscriptionSerializer.Meta.fields


class TokenInputSerializer(serializers.Serializer):
    token = serializers.CharField()


class EmailInputSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CodeInputSerializer(serializers.Serializer):
    code = serializers.CharField()

class ProfileFilterSerializer(serializers.Serializer):
    filter = serializers.ChoiceField(choices=['is_mentor', 'is_admin', 'is_hacker', 'is_staff'])
