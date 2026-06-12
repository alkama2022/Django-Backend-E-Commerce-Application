from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.serializers import ProductSerializer
from .models import Product
# Create your views here.

# Create your views here.

@api_view(['GET'])
def product_list(request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)