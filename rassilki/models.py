from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

NULLABLE = {'null': True, 'blank': True}

# Модель Клиент сервиса
class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'



# Модель рассылки
class MailingMessage(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField(max_length=255)
    FREQUENCY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )
    FIRST_CHOICES = (
        ('1', 'закончить'),
        ('2', 'сохранить'),
        ('3', 'запустить'),
    )

    send_time = models.TimeField(verbose_name='Send time', null=True, default=None, )
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    status = models.CharField(choices=FIRST_CHOICES, verbose_name='Status',
                                           default='3')
    client = models.ForeignKey(Client, verbose_name='Clients', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.body}"

    # def get_next_time_run(self) -> datetime:
    #     """Return next time run"""
    #     now = timezone.now()
    #     if self.send_time >= now.time():
    #         # Если время отправки больше или равно текущему времени сейчас, отправляем сегодня
    #         next_datetime = now.today()
    #     else:
    #         # Иначе отправляем завтра
    #         next_datetime = now.today() + timedelta(days=1)
    #
    #         # Далее добавляем интервал в зависимости от выбранной периодичности
    #         if self.frequency == 'daily':
    #             pass  # Оставляем без изменений, так как уже учтено в вычислениях выше
    #         elif self.frequency == 'weekly':
    #             next_datetime += timedelta(weeks=1)
    #         elif self.frequency == 'monthly':
    #             next_datetime += timedelta(days=30)  # Простое добавление дней
    #
    #         # Объединяем полученное дату и время отправки, чтобы получить полное время отправки
    #         next_time_run = datetime.combine(next_datetime, self.send_time)
    #
    #         return next_time_run

    # def send_email(self):
    #     subject = self.subject
    #     message = self.body
    #     from_email = "2402as@gmail.com"
    #     recipient_list = [self.client.email]
    #
    #     try:
    #         send_mail(subject, message, from_email, recipient_list)
    #
    #         # лог записи об успешной отправке
    #         Log.objects.create(
    #             log_status=Log.STATUS_SUCCESSFUL,
    #             log_client=self.client,
    #             log_mailing=self,
    #             log_server_response="Письмо успешно отправлено",
    #         )
    #
    #         return True  # Письмо успешно отправлено
    #     except Exception as e:
    #         print(f"Ошибка при отправке письма: {str(e)}")
    #
    #
    #
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


# Модель логов
class Log(models.Model):
    STATUS_SUCCESSFUL = 'SUCCESS'
    STATUS_FAILED = 'FAILED'

    STATUS_CHOICES = (
            (STATUS_SUCCESSFUL, 'Success'),
            (STATUS_FAILED, 'Failed'),
        )

    log_created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Time', **NULLABLE, )
    log_status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='Status', **NULLABLE)
    log_client = models.ForeignKey(Client, on_delete=models.SET_NULL, verbose_name='Client', **NULLABLE, )
    log_mailing = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name='Mailing', **NULLABLE, )
    log_server_response = models.TextField(**NULLABLE, verbose_name='Server response', )

    def __str__(self):
        return f"{self.log_client} - {self.log_status}"

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'


