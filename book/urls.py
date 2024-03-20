from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'confirm', OrderViewSet)


urlpatterns = [
    path('order', CreateOrder, name = 'order'),
    path('', include(router.urls)),
]
