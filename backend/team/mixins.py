from django.views.generic.base import ContextMixin
from django.shortcuts import reverse
import json


class TeamContextMixin(ContextMixin):
    """Team context mixin

    Inherit this mixin to get team data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_context = {
            "api": {
                "create_team": reverse("team:api:team-list"),
                "get_team": reverse("team:api:team-detail", args=[0])[:-2],
                "update_team": reverse("team:api:team-detail", args=[0])[:-2],
                "leave_team": reverse("team:api:team-leave-team"),
                "current_team": reverse("team:api:team-current-team"),
            }
        }
        context["team_context"] = json.dumps(team_context)
        return context
