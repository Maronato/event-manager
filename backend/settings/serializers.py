from rest_framework import serializers
from .models import Settings


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = [
            "max_hackers",
            "default_hacker",
            "default_staff",
            "auto_admit_hackers",
            "registration_opened",
            "registration_is_open",
            "can_confirm",
            "is_full",
            "hackathon_is_happening",
            "hackathon_ended",
            "registration_open_seconds",
            "registration_close_seconds",
            "confirmation_seconds",
            "hackathon_start_seconds",
            "hackathon_end_seconds",
            "ticket_expire",
            "ticket_queue_open",
            "verify_email",
            "require_payment",
            "ticket_price",
            "max_team_size",
        ]
