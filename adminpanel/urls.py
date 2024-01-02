from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomTypeViewSet, RoomViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'roomtypes', RoomTypeViewSet)
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
