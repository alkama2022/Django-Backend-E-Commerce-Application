from django_filters.rest_framework import FilterSet, filters
from . import models

class ProductFilter(FilterSet):
    # price = filters.RangeFilter()
    class Meta:
        model = models.Product
        fields = {
            'collection_id': ['exact'],
            'price': ['gt', 'lt']
        }