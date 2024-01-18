from django.contrib.auth.models import User 
from logging import exception, warn
from django.db.models.fields import return_None
from rest_framework import viewsets, permissions, authentication, exceptions
from .models import Hotel, RoomType, Room
from .serializers import HotelSerializer, RoomTypeSerializer, RoomSerializer, AdminLoginSerializer
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer 
    permission_classes = [permissions.IsAdminUser]

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer 

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer 
'''
class AdminLoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminLoginSerializer 

    def authentication(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")
        return (user, None)
  ''' 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user._id
        token['email'] = user.email
        # ...

        return token



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

