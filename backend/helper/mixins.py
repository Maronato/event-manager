from django.views.generic.base import ContextMixin
from django.shortcuts import reverse
import json


class HelperContextMixin(ContextMixin):
    """Helper context mixin

    Inherit this mixin to get helper data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        helper_context = {
            "api": {
                "last_ticket": reverse("helper:api:ticket-last-ticket"),
                "list_tickets": reverse("helper:api:ticket-list"),
                "online_mentors": reverse("helper:api:online_mentors-list"),
                "list_mentors": reverse("helper:api:mentor-list"),
                "self_mentor": reverse("helper:api:self_mentor"),
            }
        }
        context["helper_context"] = json.dumps(helper_context)
        return context
