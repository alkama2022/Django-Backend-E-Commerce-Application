from django.db.models.aggregates import Count
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.serializers import ProductSerializer,CollectionSerializers
from .models import Product,Collection
from pprint import pprint
# Create your views here.

# Create your views here.

class ProductList(APIView):
    def get(self,request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetails(APIView):
    def get(self,request,pk):
        queryset = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(queryset)
        return Response(serializer.data)
    def put(self,request,pk):
        queryset = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    def delete(self,request,pk):
        queryset = get_object_or_404(Product,pk=pk)
        if queryset.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_400_BAD_REQUEST)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionList(APIView):
    def get(self,request):
        queryset = Collection.objects.annotate(products_count=Count('product')).all()
        serializer = CollectionSerializers(queryset, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = CollectionSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetails(APIView):
    def get(self,request,pk):
        queryset = get_object_or_404(Collection,pk=pk)
        serializer = CollectionSerializers(queryset)
        return Response(serializer.data)
    
    def put(self,request,pk):
        queryset = get_object_or_404(Collection,pk=pk)
        serializer = CollectionSerializers(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    def delete(self,request,pk):
        queryset = get_object_or_404(Collection,pk=pk)
        if queryset.product_set.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it is associated with a product.'}, status=status.HTTP_400_BAD_REQUEST)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)