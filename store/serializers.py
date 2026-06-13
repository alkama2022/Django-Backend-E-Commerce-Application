from rest_framework import serializers
from . import models
from decimal import Decimal

class CollectionSerializers(serializers.ModelSerializer):
  class Meta:
    model = models.Collection
    fields = ['id','title']

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Product
    fields = ['id','title','inventory','slug','price','price_with_tax','collection']
    
  # unit_price = serializers.DecimalField(max_digits=6,decimal_places=2, source = 'price')
  price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
  collection = serializers.PrimaryKeyRelatedField(queryset=models.Collection.objects.all())
  # collection = serializers.HyperlinkedRelatedField(
  #   queryset = models.Collection.objects.all(),
  #   view_name = 'collection-details'
  # )
  def calculate_tax(self,product:models.Product):
      return product.price * Decimal(1.04)