from logging import warn
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomTypeViewSet, RoomViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'roomtypes', RoomTypeViewSet)
router.register(r'rooms', RoomViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
]
