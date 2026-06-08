from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin,models
from tags.models import TaggedItem


class TagInline(GenericTabularInline):
  autocomplete_fields = ['tag']
  model = TaggedItem
  

class CustomProductAdmin(ProductAdmin):
  inlines = [TagInline]
  
admin.site.unregister(models.Product)
admin.site.register(models.Product,CustomProductAdmin)
