import logging
import os
import smtplib
from email.mime.text import MIMEText

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


    # Получить все объекты MailingMessage
    all_mailings = MailingMessage.objects.all()

    # Вывести send_time для каждого объекта
    for mailing_info in all_mailings:
        print(f"send_time для объекта {mailing_info.pk}: {mailing_info.send_time}")

    for mailing in ready_to_mail_list:
        send_one_message(mailing.pk)



def send_one_message(mailing_pk):
    mailing = MailingMessage.objects.get(pk=mailing_pk)
    recipient_email = mailing.client.email

    try:
        if recipient_email:
            send_mail(
                mailing.subject,
                mailing.body,
                settings.EMAIL_HOST_USER,
                [recipient_email],
                settings.EMAIL_HOST,
                settings.EMAIL_PORT,
                settings.EMAIL_HOST_PASSWORD,

            )
            s = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            s.sendmail(settings.EMAIL_HOST_USER, [recipient_email], MIMEText.as_string())
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

send_mails()
