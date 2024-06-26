from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'orderconfirm', OrderViewSet)
# router.register(r'bookingconfirm', BookingViewSet)

urlpatterns = [
    # path('order', CreateOrder, name = 'order'),
    path('', include(router.urls)),
    path('create-order/', create_order, name='create-order'),
    path('order-details/<int:order_id>/', get_order_details, name='get-order-details'),
    path('mark-order-paid/', mark_order_paid, name='mark-order-paid'),

]
