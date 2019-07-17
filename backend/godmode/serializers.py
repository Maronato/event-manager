from rest_framework import serializers


class UserCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()


class BatchUserSerializer(serializers.Serializer):
    users = UserCreateSerializer(many=True)
    send_emails = serializers.BooleanField()
