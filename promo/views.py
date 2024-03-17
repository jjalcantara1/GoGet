from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Promo
from rest_framework import generics
from .serializers import PromoSerializer
class PromoListCreate(generics.ListCreateAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

class PromoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

class RedeemPromoCode(APIView):
    def post(self, request):
        promo_code = request.data.get('promo_code')
        try:
            promo = Promo.objects.get(code=promo_code)
        except Promo.DoesNotExist:
            return Response({"error": "Invalid promo code"}, status=status.HTTP_400_BAD_REQUEST)

        if promo.times_redeemed < promo.max_redemptions:
            promo.times_redeemed += 1
            promo.save()
            return Response({"discount": promo.discount}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Promo code has reached its maximum redemption limit"},
                            status=status.HTTP_400_BAD_REQUEST)