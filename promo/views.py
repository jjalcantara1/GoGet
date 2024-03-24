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

        return Response({"discount": promo.discount}, status=status.HTTP_200_OK if promo.discount else status.HTTP_400_BAD_REQUEST)
