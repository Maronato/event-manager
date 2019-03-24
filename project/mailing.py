from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class EMail(object):

    fr = settings.DEFAULT_FROM_EMAIL
    event_name = settings.EVENT_NAME
    event_url = settings.ROOT_URL
    facebook_handle = settings.FACEBOOK_HANDLE

    def __init__(self, to, subject='', title='', subtitle='', description='', action_url='', action_name=''):
        self.subject = subject
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.to = to if isinstance(to, list) else [to]
        self.action_name = action_name
        self.action_url = action_url

    def build_context(self):
        email_kargs = {
            'event_name': self.event_name
        }
        context = {
            'title': self.title.format(**email_kargs),
            'subtitle': self.subtitle.format(**email_kargs),
            'description': self.description.format(**email_kargs),
            'actionUrl': self.event_url + self.action_url,
            'actionName': self.action_name,
            'project_url': self.event_url,
            'hackathon_name': self.event_name,
            'facebookHandle': self.facebook_handle
        }
        return context

    def send_action(self):
        context = self.build_context()
        msg_plain = render_to_string('project/email/action/text.txt', context)
        msg_html = render_to_string('project/email/action/html.html', context)
        send_mail(
            f'[{self.hack_name}] {self.subject}',
            msg_plain,
            self.fr,
            self.to,
            html_message=msg_html,
        )

    def send_basic(self):
        context = self.build_context()
        msg_plain = render_to_string('project/email/basic/text.txt', context)
        msg_html = render_to_string('project/email/basic/html.html', context)
        send_mail(
            f'[{self.hack_name}] {self.subject}',
            msg_plain,
            self.fr,
            self.to,
            html_message=msg_html,
        )
