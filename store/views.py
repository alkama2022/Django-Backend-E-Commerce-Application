from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from . import models
from . import serializers

class ProductViewSet(ModelViewSet):
  queryset = models.Product.objects.all()
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['collection_id' , 'price']
  serializer_class = serializers.ProductSerilizer  
  
  def get_serializer_context(self):
     return {'request' : self.request}
   
  def destroy(self, request, *args, **kwargs):
    if models.OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
      return Response({"Error" : "Product Cannot be deleted becouse it is associated with order items"},status=405)
    return super().destroy(request, *args, **kwargs)
  
class CollectionViewSet(ModelViewSet):
  queryset = models.Collection.objects.annotate(products_count=Count('products')).all()
  serializer_class = serializers.CollectionSerializer

  def get_serializer_context(self):
     return {'request' : self.request}
   
  def destroy(self, request, *args, **kwargs):
    if models.Product.objects.filter(collection_id = kwargs['pk']).count() > 0:
      return Response({"Error" : "Collection Cannot be deleted becouse it is associated with order Product"},status=405)
    return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
  def get_queryset(self):
    return models.Review.objects.filter(product_id = self.kwargs['product_pk'])
 
  serializer_class = serializers.ReviewSerializer
  
  def get_serializer_context(self):
    return {'request' : self.kwargs['product_pk']}
  