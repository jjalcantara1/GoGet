from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from contact.views import *

urlpatterns = [
    path('contact/', ContactView.as_view(), name = "Contact Us"),
    path('contacts/', ContactListView.as_view(), name="Contact Us"),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
]