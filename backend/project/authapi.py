from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_jwt.views import (
    RefreshJSONWebToken,
    ObtainJSONWebToken,
    VerifyJSONWebToken,
)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class RefreshJWT(RefreshJSONWebToken):
    """Atualizar JWT

    Te permite atualizar um JWT que está próximo de expirar. Você pode
    atualizar um JWT até uma semana depois de ele ter sido criado.
    """

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ObtainJWT(ObtainJSONWebToken):
    """Login com JWT

    Te permite obter um token JWT novo a partir do login de um usuário.

    Você deve fornecer o usuário e a senha de um usuário válido para obter um
    token. Tokens têm validade de 1 hora e, após esse período, devem ser
    atualizados pelo endpoint de atualização.

    > Atenção: Tokens de usuários são interpretados como logins diretos desses
    usuários, logo compartilham as mesmas permissões e contextos que seus
    usuários de origem.
    """

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginWithJWT(ObtainJSONWebToken):
    """Login com JWT

    Te permite obter um token JWT novo a partir do login de um usuário.

    Você deve fornecer o usuário e a senha de um usuário válido para obter um
    token. Tokens têm validade de 1 hora e, após esse período, devem ser
    atualizados pelo endpoint de atualização.

    > Atenção: Tokens de usuários são interpretados como logins diretos desses
    usuários, logo compartilham as mesmas permissões e contextos que seus
    usuários de origem.
    """

    def post(self, request, *args, **kwargs):
        return Response(request.data)


class VerifyJWT(VerifyJSONWebToken):
    """Verificar JWT

    Te permite fazer uma introspecção em um token JWT gerado para verificar se
    ele é válido.

    Retorna 200 se for válido e 400 se for inválido.
    """

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
