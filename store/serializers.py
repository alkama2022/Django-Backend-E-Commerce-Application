from rest_framework import serializers
from . import models

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Product
    fields = ['id', 'title', 'slug', 'description', 'price', 'inventory', 'last_updated']