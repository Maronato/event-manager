from rest_framework import serializers


class UniqueIDSerializer(serializers.Serializer):
    unique_id = serializers.CharField()
