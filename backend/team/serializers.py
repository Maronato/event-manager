from rest_framework import serializers
from project.mixins import PrefetchMixin, SingleInstancePrefetchMixin
from .models import Team


class SimpleTeamSerializer(PrefetchMixin, serializers.ModelSerializer):

    members = serializers.ListField(child=serializers.CharField(), required=False)

    def create(self, validated_data):
        team_name = validated_data.get("name", None)
        if Team.objects.filter(name=team_name):
            team = Team.objects.get(name=team_name)
            if not team.allow_new or team.is_full:
                raise serializers.ValidationError(
                    {"message": "Equipe fechada ou cheia"}
                )
                return Team.objects.empty()
        else:
            team = self.Meta.model.objects.create(**validated_data)

        team.add_hacker(self.context["request"].user.profile.hacker)
        return team

    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = ["id", "members"]


class TeamSubscriptionSerializer(SingleInstancePrefetchMixin, SimpleTeamSerializer):
    """Allow single instance prefetching"""
