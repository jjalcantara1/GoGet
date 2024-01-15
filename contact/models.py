from django.db import models
from django.core.mail import send_mail
# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, help_text='Enter the name', verbose_name='Name')
    email = models.EmailField(null=False, blank=False, help_text='Enter the email', verbose_name='Email')
    subject = models.CharField(max_length=255, null=False, blank=False, help_text='Subject', verbose_name='Subject')
    message = models.CharField(max_length=255, null=False, blank=False, help_text='Message', verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.subject
