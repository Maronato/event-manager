from .emails import verify_email, recover_token_email
from celery import shared_task


@shared_task
def send_verify_email(profile_id):
    from .models import Profile

    profile = Profile.objects.get(id=profile_id)
    return verify_email(profile)


@shared_task
def send_verify_email_batch(user_ids):
    for uid in user_ids:
        send_verify_email.delay(uid)


@shared_task
def send_recover_token_email(profile_id):
    from .models import Profile

    profile = Profile.objects.get(id=profile_id)
    return recover_token_email(profile)
