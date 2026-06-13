from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Count
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from store.serializers import ProductSerializer,CollectionSerializers, ReviewSerializer
from .models import OrderItem, Product,Collection, Review
from .filters import ProductFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    search_fields = ['title','description']
    ordering_fields = ['price','last_updated']
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self,request,*args,**kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with one or more order items.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request,*args,**kwargs)
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializers
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self,request,*args,**kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request,*args,**kwargs)
    

class ReviewViewSet(ModelViewSet):
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    serializer_class = ReviewSerializer
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
