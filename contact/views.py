import output
from GoGet import settings
from .models import *
from .serializer import *

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

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

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact_message = serializer.save()

            # Send contact email
            email = EmailMessage(
                subject=serializer.validated_data['subject'],
                body=f"Name: {serializer.validated_data['name']}\n"
                     f"{serializer.validated_data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],  # Ensure this is a list or tuple
                reply_to=[serializer.validated_data['email']],  # Sender's address
            )
            email.send(fail_silently=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return success response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return error response