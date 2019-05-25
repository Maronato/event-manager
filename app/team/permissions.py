from hacker.permissions import IsHacker


class IsTeamMember(IsHacker):

    def has_permission(self, request, view):
        is_hacker = super().has_permission(request, view)
        if is_hacker:
            try:
                team = view.get_object()
            except AssertionError:
                # If not retrieve, team is None
                team = None
            hacker = request.user.profile.hacker
            if team is None:
                return getattr(hacker, 'team', None) is not None
            return getattr(hacker, 'team', None) == team
        return False
