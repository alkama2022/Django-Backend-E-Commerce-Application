from rest_framework import serializers
from . import models
from decimal import Decimal

class CollectionSerializers(serializers.ModelSerializer):
  class Meta:
    model = models.Collection
    fields = ['id','title','products_count']
  products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Product
    fields = ['id','title','inventory','slug','price','price_with_tax','collection']
    
  price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
  collection = serializers.PrimaryKeyRelatedField(queryset=models.Collection.objects.all())
  def calculate_tax(self,product:models.Product):
      return product.price * Decimal(1.04)