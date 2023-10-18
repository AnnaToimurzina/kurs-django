import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from django import forms
from .models import Client, MailingMessage


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']



class MailingMessageForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = ['subject', 'body', 'send_time', 'frequency', 'status', 'client']


