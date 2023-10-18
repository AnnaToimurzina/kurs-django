import logging
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.utils import timezone
from smtplib import SMTPException

from config import settings
from config.celery import app
from celery import Task

from rassilki.models import MailingMessage, Log


class MailingTask(Task):
    autoretry_for = (SMTPException,)
    max_retries = 3
    ignore_result = True


def send_mails() -> None:
    """Send email to clients"""
    logging.info('функция стартовала')
    now = timezone.now()

    ready_to_mail_list = MailingMessage.objects.filter(send_time='01:45')
    count = len(ready_to_mail_list)

    if count > 0:
        print(f"Есть {count} объектов для отправки.")
    else:
        print("Нет объектов для отправки.")

    for mailing in ready_to_mail_list:
        send_one_message.delay(mailing.pk)




def send_one_message(mailing_pk: int) -> None:
    mailing: MailingMessage = MailingMessage.objects.get(pk=mailing_pk)
    recipient_email: list[str] = [client.email for client in mailing.client.all()]

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
            for client in mailing.client.all():

                log = Log(
                    log_status=Log.STATUS_SUCCESSFUL,
                    log_client=client,
                    log_mailing=mailing,
                    log_server_response='Email Sent Successfully!',
                )
                logs.append(log)
            Log.objects.bulk_create(logs)

    except SMTPException as err:
        logs =[]
        for client in mailing.client.all():
            log = Log(
                log_status=Log.STATUS_FAILED,
                log_client=client,
                log_mailing=mailing,
                log_server_response=err,
            )
            logs.append(log)
        Log.objects.bulk_create(logs)

        raise
    print(f"Отправка сообщения для Mailing PK {mailing_pk}")

send_mails()


# Получить все объекты MailingMessage
all_mailings = MailingMessage.objects.all()

# Вывести send_time для каждого объекта
for mailing in all_mailings:
    print(f"send_time для объекта {mailing.pk}: {mailing.send_time}")

