import output
from django.shortcuts import render
from rest_framework.views import APIView

from GoGet import settings
from .models import *
from rest_framework.response import Response
from .serializer import *
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics


# Create your views here.

class ContactListView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactDetailView(generics.RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


def send_contact_email(data):
    subject = data['subject']
    message = f'''
    Name: {data['name']}
    Email: {data['email']}
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
