from rest_framework import permissions


class IsHacker(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.profile.is_hacker


class IsCheckedin(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'checkedin'


class IsAdmitted(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'admitted'


class IsConfirmed(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'confirmed'


class IsWithdraw(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'withdraw'


class IsSubmitted(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'submitted'


class IsIncomplete(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'incomplete'


class IsUnpayed(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and not request.user.profile.hacker.payed
