from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
    path('available-room-types/', available_room_types, name='available-room-types'),
    path('room-types-availability/', room_types_availability, name='room-types-availability'),

]
