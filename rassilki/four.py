import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings')
import django
django.setup()

from django.core.mail import send_mail
from django.utils import timezone
from smtplib import SMTPException

from config import settings
from celery import Task

from rassilki.models import MailingMessage, Log, Client


class MailingTask(Task):
    autoretry_for = (SMTPException,)
    max_retries = 3
    ignore_result = True


def send_mails() -> None:
    """Send email to clients"""
    now = timezone.now()
    ready_to_mail_list = MailingMessage.objects.filter(send_time=now)

    for mailing in ready_to_mail_list:
        send_one_message.delay(mailing.pk)



def send_one_message(mailing_pk: int) -> None:
    mailing: MailingMessage = MailingMessage.objects.get(pk=mailing_pk)
    recipient_email: list[str] = [client.email for client in mailing.mail_client.all()]

    try:
        if recipient_email:
            send_mail(
                mailing.subject,
                mailing.body,
                settings.EMAIL_HOST_USER,
                recipient_email,
                fail_silently=False,
            )
            logs = []
            for client in mailing.mail_client.all():
                log = Log(
                    log_status=Log.STATUS_SUCCESSFUL,
                    log_client=mailing.client,
                    log_mailing=mailing,
                    log_server_response='Email Sent Successfully!',
                )
                log.save()

                print(f"Рассылка с темой '{mailing.subject}' была успешно отправлена.")
    except Exception as e:
        print(f"Ошибка отправки письма: {str(e)}")



        logs.append(log)

send_mails()


