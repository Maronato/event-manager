from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.messages import get_messages
from rest_framework_jwt.settings import api_settings
from .providers import facebook, github, google
from .util import decode_state_data, login_canceled


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.
providers = {
    'facebook': facebook,
    'github': github,
    'google': google,
}


def build_url(url, request):
    parts = list(urlparse(url))
    query = parse_qs(parts[4])
    params = {
        "messages": [],
        "errors": []
    }
    for message in get_messages(request):
        tag = message.level_tag
        text = message.message
        if tag in ['error', 'warning']:
            params['errors'].append(text)
        else:
            params['messages'].append(text)
    if request.user.is_authenticated:
        params['token'] = jwt_encode_handler(jwt_payload_handler(request.user))
    query.update(params)
    parts[4] = urlencode(query, True)
    return urlunparse(parts)


class SocialLogin(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        provider = providers[kwargs['provider']]
        return provider.auth_url(self.request)


class SocialLoginResponse(RedirectView):
    max_code_redirects = 3

    def get_redirect_url(self, *args, **kwargs):
        provider = providers[kwargs['provider']]
        code = self.request.GET.get('code', False)
        state_data = decode_state_data(self.request.GET.get('state', False))
        redirected = state_data.get('redirected', False)
        next_url = state_data.get('next_url', False)
        if not code or redirected and int(redirected) >= self.max_code_redirects:
            self.request = login_canceled(self.request)
            url = build_url(settings.LOGIN_REDIRECT_URL, self.request)
            return url
        else:
            response = provider.login_successful(code, self.request)
            if response == 'auth code used' or response == 'token missing':
                # if the auth code has already been used, redirect
                url = build_url(provider.code_already_used_url(next_url, redirected), self.request)
                return url
            self.request = response
        if next_url:
            return next_url
        url = build_url(settings.LOGIN_REDIRECT_URL, self.request)
        return url
