from rest_framework.permissions import IsAuthenticated
from rest_framework import views, mixins, viewsets


class UnlinkProvider(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        provider = request.data.get("provider")
        profile = request.user.profile
        profile.unlink_social_provider(provider)
        return views.Response({"message": f"{provider} removido"}, status=200)
