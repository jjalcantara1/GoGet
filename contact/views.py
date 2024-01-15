import output
from django.shortcuts import render
from rest_framework.views import APIView

from GoGet import settings
from .models import *
from rest_framework.response import Response
from .serializer import *
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def send_contact_email(data):
    subject = 'Query'
    message = f'''
    Name: {data['name']}
    Email: {data['email']}
    Subject: {data['subject']}
    Message: {data['message']}
    '''

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Sender's email address
        [settings.EMAIL_HOST_USER],  # Receiver's email address (can be a list of multiple emails)
        fail_silently=False,
    )


class ContactView(APIView):
    serializer_class = ContactSerializer

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        # subject = models.Contact.subject

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_contact_email(serializer.validated_data)

            return Response(serializer.data)
