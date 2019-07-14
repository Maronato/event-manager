from rest_framework.generics import RetrieveAPIView
from user_profile.serializers import SelfSubscriptionSerializer


class MeView(RetrieveAPIView):
    """Detalhes do usuário

    Permite acessar detalhes do usuário logado.
    """

    serializer_class = SelfSubscriptionSerializer

    def get_object(self):
        return self.request.user.profile

    def retrieve(self, *args, **kwargs):
        """Detalhes do usuário

        Permite acessar detalhes do usuário logado.
        """
        return super().retrieve(*args, **kwargs)
