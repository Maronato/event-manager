from django.urls import reverse
from project.mailing import EMail


def verify_email(profile):
    email = EMail(
        to=profile.user.email,
        subject='Verificar email',
        title='Verificação de Email',
        description='Você está recebendo essa mensagem pois alterou seu email.<br><br>Use o botão abaixo para verificar seu email:',
        action_name='Verificar email',
        action_url=reverse('profile:verify_email', args={profile.verification_code}),
    )
    email.send_action()


def recover_token_email(profile):
    email = EMail(
        to=profile.user.email,
        subject='Recuperar Token',
        title='Recuperar token',
        description='Você está recebendo essa mensagem pois alguém pediu para que o seu token fosse recuperado.<br><br>Seu token atual é <b>{profile.token}</b> e você pode logar em sua conta usando o botão abaixo',
        action_name='Acessar sua conta',
        action_url=reverse('profile:token_login', args={profile.token}),
    )
    email.send_action()
