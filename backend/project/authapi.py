from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework_jwt.views import (
    RefreshJSONWebToken,
    ObtainJSONWebToken,
    VerifyJSONWebToken,
)
from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


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
        payload = jwt_decode_handler(request.data.get('token'))
        username = jwt_get_username_from_payload(payload)
        user = User.objects.get_by_natural_key(username)
        login(request, user)
        return Response(request.data)


class VerifyJWT(VerifyJSONWebToken):
    """Verificar JWT

    Te permite fazer uma introspecção em um token JWT gerado para verificar se
    ele é válido.

    Retorna 200 se for válido e 400 se for inválido.
    """

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class Logout(APIView):

    def get(self, request, format=None):
        logout(request)
        return Response()
