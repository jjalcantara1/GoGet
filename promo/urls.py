from django.urls import path
from .views import *

urlpatterns = [
    path('promos/', PromoListCreate.as_view(), name='promo-list-create'),
    path('promos/<int:pk>/', PromoRetrieveUpdateDestroy.as_view(), name='promo-retrieve-update-destroy'),
    path('redeem-promo/', RedeemPromoCode.as_view(), name='redeem-promo'),
]