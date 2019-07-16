from django.conf import settings


def event_info(request):
    return {
        "EVENT_NAME": settings.EVENT_NAME,
        "EVENT_DESCRIPTION": settings.EVENT_DESCRIPTION,
    }
