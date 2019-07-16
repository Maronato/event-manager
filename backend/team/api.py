from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_condition import And, Or
from project.permissions import IsPostRequest, IsGetRequest, IsPutPatchRequest
from settings.permissions import EventIsHappening
from hacker.permissions import IsCheckedin
from project.mixins import PrefetchQuerysetModelMixin
from .permissions import IsTeamMember
from .models import Team
from .serializers import SimpleTeamSerializer


class TeamViewset(
    PrefetchQuerysetModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [
        Or(
            And(IsPostRequest, IsCheckedin, EventIsHappening),  # Creating new teams
            And(IsGetRequest, IsCheckedin, IsTeamMember),  # Getting teams
            And(IsPutPatchRequest, EventIsHappening, IsTeamMember),  # Updating teams
        )
    ]
    queryset = Team.objects.all()
    serializer_class = SimpleTeamSerializer

    @action(methods=["post"], detail=False)
    def leave_team(self, request):
        hacker = request.user.profile.hacker
        team = getattr(hacker, "team", None)
        if team:
            team.remove_hacker(hacker)
            if len(team.members) == 0:
                team.delete()
        return Response(status=200)

    @action(methods=["get"], detail=False)
    def current_team(self, request):
        hacker = request.user.profile.hacker
        team = hacker.team
        serializer = self.get_serializer_class()(team)
        data = serializer.data
        return Response(data)
