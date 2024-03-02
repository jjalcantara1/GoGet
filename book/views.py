from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

@api_view(['POST'])
def CreateOrder(request):
        data = request.data
        print(data['contact_number'])
        order = Order.objects.create(
                name = data['name'],
                email = data['email'],
                contact_number = data['contact_number']
                )
        serializer = OrderSerializer(order, many=False)
        return Response({'message: success'})
