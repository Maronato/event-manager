import json
from django.conf import settings
from django.contrib.messages.storage.cookie import CookieStorage
from django.contrib.messages.storage.base import Message
from django.contrib.messages import constants
from django.utils.safestring import SafeData, mark_safe


class MessageEncoder(json.JSONEncoder):
    """
    Compactly serialize instances of the ``Message`` class as JSON.
    """

    message_key = "__json_message"

    def default(self, obj):
        if isinstance(obj, Message):
            # Using 0/1 here instead of False/True to produce more compact json
            is_safedata = 1 if isinstance(obj.message, SafeData) else 0
            message = [
                self.message_key,
                is_safedata,
                constants.DEFAULT_TAGS[obj.level],
                obj.message,
            ]
            if obj.extra_tags:
                message.append(obj.extra_tags)
            return message
        return super().default(obj)


class MessageDecoder(json.JSONDecoder):
    """
    Decode JSON that includes serialized ``Message`` instances.
    """

    def process_messages(self, obj):
        if isinstance(obj, list) and obj:
            if obj[0] == MessageEncoder.message_key:
                if len(obj) == 3:
                    # Compatibility with previously-encoded messages
                    return Message(*obj[1:])
                if obj[1]:
                    obj[3] = mark_safe(obj[3])
                return Message(constants.DEFAULT_LEVELS[obj[2].upper()], *obj[3:])
            return [self.process_messages(item) for item in obj]
        if isinstance(obj, dict):
            return {key: self.process_messages(value) for key, value in obj.items()}
        return obj

    def decode(self, s, **kwargs):
        decoded = super().decode(s, **kwargs)
        return self.process_messages(decoded)


class JavascripAccessibleMessageStorage(CookieStorage):
    def _update_cookie(self, encoded_data, response):
        """
        Either set the cookie with the encoded data if there is any data to
        store, or delete the cookie.
        """
        if encoded_data:
            response.set_cookie(
                self.cookie_name,
                encoded_data,
                domain=settings.SESSION_COOKIE_DOMAIN,
                secure=settings.SESSION_COOKIE_SECURE or None,
                httponly=False,
                samesite=settings.SESSION_COOKIE_SAMESITE,
            )
        else:
            response.delete_cookie(
                self.cookie_name, domain=settings.SESSION_COOKIE_DOMAIN
            )

    def _encode(self, messages, encode_empty=False):
        if messages or encode_empty:
            return json.dumps(messages, cls=MessageEncoder)

    def _decode(self, data):
        if not data:
            return None
        return json.loads(data, cls=MessageDecoder)
