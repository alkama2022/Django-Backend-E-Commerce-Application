from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count

from .filters import ProductFilter
from .pagination import DefaultPagination
from . import models
from . import serializers

class ProductViewSet(ModelViewSet):
  queryset = models.Product.objects.all()
  filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
  filterset_class = ProductFilter
  pagination_class = DefaultPagination
  serializer_class = serializers.ProductSerilizer  
  search_fields = ['title','description']
  ordering_fields = ['price','last_update']
  
  def get_serializer_context(self):
     return {'request' : self.request}
   
  def destroy(self, request, *args, **kwargs):
    if models.OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
      return Response({"Error" : "Product Cannot be deleted becouse it is associated with order items"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return super().destroy(request, *args, **kwargs)
  
class CollectionViewSet(ModelViewSet):
  queryset = models.Collection.objects.annotate(products_count=Count('products')).all()
  serializer_class = serializers.CollectionSerializer

  def get_serializer_context(self):
     return {'request' : self.request}
   
  def destroy(self, request, *args, **kwargs):
    if models.Product.objects.filter(collection_id = kwargs['pk']).count() > 0:
      return Response({"Error" : "Collection Cannot be deleted becouse it is associated with order Product"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
  def get_queryset(self):
    return models.Review.objects.filter(product_id = self.kwargs['product_pk'])
 
  serializer_class = serializers.ReviewSerializer
  
  def get_serializer_context(self):
    return {'request' : self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin,RetrieveModelMixin,GenericViewSet):
  queryset = models.Cart.objects.all()
  serializer_class = serializers.CartSerializer

class CartItemViewSet(ModelViewSet):
  serializer_class = serializers.CartItemSerializer
  def get_queryset(self):
    return models.CartItem.objects.filter(
        cart_id=self.kwargs['carts_pk']
    )
  def get_serializer_context(self):
    return {
        'cart_id': self.kwargs['carts_pk']
    }
  
  

