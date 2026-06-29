from decimal import Decimal
from rest_framework import serializers
from . import models



class CollectionSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Collection
    fields = ['id','title','products_count']
  
  products_count = serializers.IntegerField(read_only = True)
    
class ProductSerilizer(serializers.ModelSerializer):
  price_with_text = serializers.SerializerMethodField(method_name='calculate_tex')
  
  def calculate_tex(self,product : models.Poduct):
      return product.price * Decimal(1.01)
  
  class Meta:
    model = models.Product
    fields = ['id','title','slug','inventory','description','price','price_with_text','collection']

class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Review
    fields = ['id','date','name','description']
  
  def create(self, validated_data):
    product_id = self.context['product_id']
    return models.Review.objects.create(product_id=product_id,**validated_data)
class SimpleProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Product
    fields = ['id','title','price']
    
    
    
    
class CartItemSerializer(serializers.ModelSerializer):
    product_detail = SimpleProductSerializer(source='product', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity
      
      
    def create(self, validated_data):
      cart_id = self.context['cart_id']
      product = validated_data['product']
      quantity = validated_data['quantity']
      
      item, created = models.CartItem.objects.get_or_create(
        cart_id=cart_id,
        product=product,
        defaults={'quantity': quantity}
    )
      
      if not created:
        item.quantity += quantity
        item.save()
      
      return item
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(
            item.product.price * item.quantity
            for item in obj.items.all()
        )
        

class UpdateCartItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.CartItem
    fields = ['quantity']
    
class CustomerSerializer(serializers.ModelSerializer):
  user_id = serializers.IntegerField(read_only=True)
  class Meta:
    model = models.Customer
    fields = ['id','user_id','phone_number','birth_date','member_ship']

class OrderItemSerialize(serializers.ModelSerializer):
  product = SimpleProductSerializer()
  # order_id = serializers.IntegerField()
  class Meta:
    model = models.OrderItem
    fields = ['id','product','quantity','unit_price']
              

class OrderSerializer(serializers.ModelSerializer):
  items = OrderItemSerialize(many=True)
  class Meta:
    model = models.Order
    fields = ['id','customer','placed_at','payment_status','items']


class CreateOrderSerializer(serializers.Serializer):
  cart_id = serializers.UUIDField()
  
  def save(self, **kwargs):
    customer = models.Customer.objects.get(user_id=self.context['user_id'])
    order = models.Order.objects.create(customer=customer)

    cart = models.Cart.objects.get(pk=self.validated_data['cart_id'])

    cart_items = models.CartItem.objects.select_related('product').filter(cart=cart)

    order_items = [
        models.OrderItem(
            order=order,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.product.unit_price
        )
        for item in cart_items
    ]

    models.OrderItem.objects.bulk_create(order_items)
    cart.delete()

    return order