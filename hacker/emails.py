from django.urls import reverse
from project.mailing import EMail


def notify_admitted(hacker):
    email = EMail(
        to=hacker.profile.user.email,
        subject='Aplicação Aceita!',
        title='Informações importantes',
        subtitle='Leia tudo!',
        description='Avaliamos sua aplicação e queremos você no {event_name}!<br><b>Atenção!</b> Seu próximo passo é acessar seu <b>>my<</b> novamente para confirmar seu interesse em participar.<br><br><b>Não confirmar seu interesse resultará na perda de sua vaga!</b><br><br><b>Não tem interesse?</b> Declare que vai se abster para que sua vaga possa ser cedida a alguém na fila de espera.',
        action_name='Acessar sua conta',
        action_url=reverse('profile:token_login', args={hacker.profile.token})
    )
    email.send_action()


def nag_admitted(hacker):
    email = EMail(
        to=hacker.profile.user.email,
        subject='Ação necessária!',
        title='Informações importantes',
        subtitle='Leia tudo!',
        description='Avaliamos sua aplicação e queremos você no {event_name}!<br><b>Atenção!</b> Seu próximo passo é acessar seu <b>>my<</b> novamente para confirmar seu interesse em participar.<br><br><b>Não confirmar seu interesse resultará na perda de sua vaga!</b><br><br><b>Não tem interesse?</b> Declare que vai se abster para que sua vaga possa ser cedida a alguém na fila de espera.',
        action_name='Acessar sua conta',
        action_url=reverse('profile:token_login', args={hacker.profile.token})
    )
    email.send_action()


def notify_waitlist(hacker):
    email = EMail(
        to=hacker.profile.user.email,
        subject='Fila de espera',
        title='Foi por pouco!',
        subtitle='Leia tudo!',
        description='Sua aplicação para o {event_name} foi aceita, mas infelizmente nós já atingimos o máximo de participantes.<br><b>Não perca as esperanças!</b> Alguém ainda pode desistir até o dia da confirmação de interesse e a vaga abrir para você.<br>Você receberá um <b>email</b> no instante que isso acontecer, então fique de olhos abertos!',
        action_name='Acessar sua conta',
        action_url=reverse('profile:token_login', args={hacker.profile.token})
    )
    email.send_action()


def notify_unwaitlist(hacker):
    email = EMail(
        to=hacker.profile.user.email,
        subject='Abriu uma vaga',
        title='Abriu uma vaga!',
        subtitle='Leia tudo!',
        description='Alguém desistiu e uma vaga foi aberta para você no {event_name}!<br><b>Atenção!</b> Seu próximo passo é acessar seu <b>>my<</b> novamente para confirmar seu interesse em participar.<br><br><b>Não confirmar seu interesse resultará na perda de sua vaga!</b><br><br><b>Não tem interesse?</b> Declare que vai se abster para que sua vaga possa ser cedida a alguém na fila de espera.<br> Para fazer isso, clique no botão abaixo:',
        action_name='Acessar sua conta',
        action_url=reverse('profile:token_login', args={hacker.profile.token})
    )
    email.send_action()


def notify_decline(hacker):
    email = EMail(
        to=hacker.profile.user.email,
        subject='Sobre sua aplicação',
        title='Sentimos muito',
        description='Avaliamos sua aplicação e infelizmente decidimos que você não poderá fazer parte dessa edição do {event_name}.<br>Esperamos ver você em edições futuras!',
    )
    email.send_basic()
