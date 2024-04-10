from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView


router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'roomtypes', RoomTypeViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('roomtypes/<int:room_type_id>/rooms/', get_rooms_by_type, name='get_rooms_by_type'),
    path('rooms/', add_room, name='add_room'),
    path('rooms/<int:room_id>/', edit_room, name='edit_room'),
    path('rooms/<int:room_id>/delete/', delete_room, name='delete_room'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('roomtypes/<int:room_type_id>/<start_date>/<end_date>/available-rooms/', get_available_rooms, name='get_available_rooms'),
    path('guest-log/', guest_log, name='guest_log'),
    path('guest-log/add-entry', add_entry, name='add-entry'),
    path('guest-log/update-entry/<int:id>', update_entry, name='update-entry'),
    path('guest-log/delete-entry/<int:id>', delete_entry, name='delete-entry'),
    path('status-choices/', StatusChoicesView.as_view(), name='status-choices'),
    path('surcharge-rates/', get_surcharge_rates, name='get_surcharge_rates'),
    path('surcharge-rates/update/', update_surcharge_rates, name='update-surcharge-rates'),

]
