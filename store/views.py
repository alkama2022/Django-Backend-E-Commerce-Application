from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.serializers import ProductSerializer,CollectionSerializers
from .models import Product,Collection
from pprint import pprint
# Create your views here.

# Create your views here.

@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def product_detail(request, pk):
    queryset = get_object_or_404(Product, pk=pk)
    if request.method == 'PUT':
        serializer = ProductSerializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = ProductSerializer(queryset)
    return Response(serializer.data)

@api_view(['GET'])
def collection_details(request,pk):
    queryset = get_object_or_404(Collection,pk=pk)
    serializer = CollectionSerializers(queryset)
    return Response(serializer.data)