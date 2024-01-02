from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/', views.admin_panel, name='admin-panel'),
    path('roomtypes/', views.RoomTypeList.as_view(), name='roomtype-list'),
    path('rooms/', views.RoomList.as_view(), name='room-list'),
    path('add-hotel/', views.add_hotel, name='add-hotel'),
    path('add-room-type/', views.add_room_type, name='add-room-type'),
]
