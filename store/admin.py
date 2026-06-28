from django.contrib import admin
from django.db.models import Count, QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

class InventoryFilter(admin.SimpleListFilter):
  title = 'inventory'
  parameter_name = 'inventory'
  
  def lookups(self, request, model_admin):
    return [
      ('<10','Low'),
      
    ]
  def queryset(self, request, queryset:QuerySet):
    if self.value() == '<10':
      return queryset.filter(inventory__lt=10)
    
  
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
  list_display = ['title','products_count']
  search_fields = ['title']
  
  @admin.display(ordering = 'product_set')
  
  def products_count(self,collection:models.Collection):
    url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection_id' : str(collection.id)})
    return format_html('<a href="{}">{}</a>',url,collection.products_count)
  
  def get_queryset(self,request):
    queryset = super().get_queryset(request).annotate(products_count = Count('product'))
    return queryset
  
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
  autocomplete_fields = ['collection']
  list_display = ('title','price','inventory_status','collection')
  list_editable = ('price',)
  list_filter = ['collection','last_updated',InventoryFilter]
  list_per_page = 5
  list_select_related = ['collection']
  prepopulated_fields = {'slug' : ['title']}
  search_fields = ['title']
  
  
  def inventory_status(self,product:models.Product):
    if product.inventory < 60 :
      return 'Low'
    return 'Ok'

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ('user__first_name','user__last_name','member_ship', 'customer_orders')
  list_editable = ('member_ship',)
  list_per_page = 5
  list_select_related = ['user']
  ordering = ['user__first_name','user__last_name']
  search_fields = ['first_name__istartswith','last_name__istartswith']
  
  
  
  def customer_orders(self,customer):
    name = ''
    if self.customer_orders != 1:
      name = 'Order'
    else : name = 'Orders'
    url=reverse('admin:store_order_changelist') + '?' + urlencode({'customer_id':str(customer.id)})
    return format_html('<a href="{}">{} {}</a>',url,customer.customer_orders,name)
     
  
  def get_queryset(self,request):
    queryset = super().get_queryset(request).annotate(customer_orders=Count('order'))
    return queryset

class OrderItemInline(admin.TabularInline):
  autocomplete_fields =['product']
  min_num = 1
  max_num = 10
  model = models.OrderItem
  extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
  autocomplete_fields = ['customer']
  inlines = [OrderItemInline]
  list_display = ['id', 'placed_at','customer']