from rest_framework.permissions import IsAuthenticated
from rest_condition import Or, And
from project.permissions import IsReadyOnlyRequest
from godmode.permissions import IsAdmin

can_see_announcements = [Or(IsAdmin, And(IsAuthenticated, IsReadyOnlyRequest))]
