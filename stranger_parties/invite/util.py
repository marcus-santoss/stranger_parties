from threading import Thread

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError


class MailContext:
    def __init__(self):
        self.subject = ""
        self.to = []
        self.cc = []
        self.bcc = []
        self.from_mail = ""
        self.template_notification = ""
        self.mail_context = {}
        self.fail_silently = False


class EmailThread(Thread):
    def __init__(self, context: MailContext):
        super(EmailThread, self).__init__()
        self.daemon = True
        self.context = context

    def send_html_email(self) -> bool:
        message = render_to_string(
            self.context.template_notification, self.context.mail_context
        )
        try:
            msg = EmailMultiAlternatives(
                subject=self.context.subject,
                body=message,
                from_email=self.context.from_mail,
                to=self.context.to,
                bcc=self.context.bcc,
                cc=self.context.cc,
            )
            msg.attach_alternative(message, "text/html")
            msg.content_subtype = "html"
            msg.send(self.context.fail_silently)

            return True
        except Exception as ex:
            raise ValidationError({
                "mail": [
                    "Não foi possível enviar a mensagem",
                    str(ex)
                ]
            })

    def run(self):
        self.send_html_email()


class HtmlMail:
    def __init__(self, context: MailContext):
        self.context = context

    def send_html_email(self) -> bool:
        message = render_to_string(
            self.context.template_notification, self.context.mail_context
        )

        try:
            msg = EmailMultiAlternatives(
                subject=self.context.subject,
                body=message,
                from_email=self.context.from_mail,
                to=self.context.to,
                bcc=self.context.bcc,
                cc=self.context.cc,
            )
            msg.attach_alternative(message, "text/html")
            msg.content_subtype = "html"
            msg.send(fail_silently=False)

            return True
        except Exception as ex:
            print(f"send_mail_context: {ex}")
            return False
