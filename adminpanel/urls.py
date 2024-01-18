from logging import warn
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomTypeViewSet, RoomViewSet, MyTokenObtainPairView

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'roomtypes', RoomTypeViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'login', MyTokenObtainPairView, basename= 'login')


urlpatterns = [
    path('', include(router.urls)),
]
