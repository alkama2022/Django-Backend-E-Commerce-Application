from rest_framework.decorators import api_view,
from rest_framework.response import Response

from django.db.models import Count
from django.shortcuts import get_object_or_404
from . import models
from . import serializers


@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET' :
      product = models.Product.objects.select_related('collection').all()
      serializer = serializers.ProductSerilizer(product, many = True,context={'request': request})
      return Response(serializer.data)
    elif request.method == "POST":
      serializer = serializers.ProductSerilizer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)



@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
  product = get_object_or_404(models.Product,pk = id)
  if request.method == 'GET':
    serializer = serializers.ProductSerilizer(product)
    return Response(serializer.data)
  elif request.method == 'PUT':
        serializer = serializers.ProductSerilizer(product,data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
  elif request.method == 'DELETE':
    if product.orderitems.count() > 0 :
      return Response({"Error" : "Product Cannot be deleted becouse it is associated with order items"},status=405)
    product.delete()
    return Response(status=204)

@api_view()

def collection_detail(request,pk):
  collection = get_object_or_404(models.Collection,pk = pk)
  serializer = serializers.CollectionSerializer(collection)
  return Response(serializer.data)

@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET' :
      collection = models.Collection.objects.annotate(products_count=Count('products')).all()
      serializer = serializers.CollectionSerializer(collection, many = True,context={'request': request})
      return Response(serializer.data)
    
    elif request.method == "POST":
      serializer = serializers.CollectionSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def collection_detail(request,id):
  collection = get_object_or_404(models.Collection,pk = id)
  if request.method == 'GET':
    serializer = serializers.CollectionSerializer(collection)
    return Response(serializer.data)
  elif request.method == 'PUT':
        serializer = serializers.CollectionSerializer(collection,data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
  elif request.method == 'DELETE':
    if collection.products.count() > 0 :
      return Response({"Error" : "Collection Cannot be deleted becouse it is associated with order Product"},status=405)
    collection.delete()
    return Response(status=204)
