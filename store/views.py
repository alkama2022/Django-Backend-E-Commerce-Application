from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django.db.models import Count

from .filters import ProductFilter
from .pagination import DefaultPagination
from . import models
from . import serializers
from .permissions import ISAdminOrReadOnly,FullDjangoModelPermissions,ViewCustomerHistoryPermission

class ProductViewSet(ModelViewSet):
  queryset = models.Product.objects.all()
  filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
  filterset_class = ProductFilter
  pagination_class = DefaultPagination
  serializer_class = serializers.ProductSerilizer  
  search_fields = ['title','description']
  ordering_fields = ['price','last_update']
  permission_classes = [ISAdminOrReadOnly]
  
  def get_serializer_context(self):
     return {'request' : self.request}
   
  def destroy(self, request, *args, **kwargs):
    if models.OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
      return Response({"Error" : "Product Cannot be deleted becouse it is associated with order items"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return super().destroy(request, *args, **kwargs)
  
class CollectionViewSet(ModelViewSet):
  queryset = models.Collection.objects.annotate(products_count=Count('products')).all()
  serializer_class = serializers.CollectionSerializer
  permission_classes = [ISAdminOrReadOnly]
  
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


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
  queryset = models.Cart.objects.prefetch_related('items__product').all()
  serializer_class = serializers.CartSerializer

class CartItemViewSet(ModelViewSet):
  http_method_names = ['get','post','patch','delete']
  def get_serializer_class(self):
   if self.request.method == 'PATCH':
     return serializers.UpdateCartItemSerializer
   return serializers.CartItemSerializer
  
  def get_queryset(self):
    return models.CartItem.objects.filter(
        cart_id=self.kwargs['cart_pk']
    ).select_related('product')
    
  def get_serializer_context(self):
    return {
        'cart_id': self.kwargs['cart_pk']
    }

class CustomerViewSet(ModelViewSet):
  queryset = models.Customer.objects.all()
  serializer_class = serializers.CustomerSerializer
  permission_classes = [IsAdminUser]
  
  
  @action(detail=True,permission_classes=[ViewCustomerHistoryPermission])
  def history(self, request, pk):
    return Response("OK")
  
  @action(detail=False, methods=['GET', 'PUT'],permission_classes=[IsAuthenticated])
  def me(self, request):
    (customer,created) = models.Customer.objects.get_or_create(user_id = request.user.id)
    if request.method == 'GET':
      serializer = serializers.CustomerSerializer(customer)
      return Response(serializer.data)
    elif request.method == 'PUT':
      serializer = serializers.CustomerSerializer(customer,data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderSerializer
        return serializers.OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return models.Order.objects.all()

        customer, created = models.Customer.objects.get_or_create(user=user)

        return models.Order.objects.filter(customer=customer)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
  
  # def me(self, request)
# class OderItemViewSet(ModelViewSet):
#   queryset = models.OrderItem.objects.all()
#   serializer_class = serializers.OrderItemSerialize