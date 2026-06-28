
from rest_framework_nested import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()

router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)

product_router = routers.NestedDefaultRouter(router,'products', lookup='product') # parents router

cart_router = routers.NestedDefaultRouter(router,'carts',lookup = 'cart')

product_router.register('reviews',views.ReviewViewSet,basename='product_reviews') #Chield Router
cart_router.register('items',views.CartItemViewSet,basename='cart_items')

urlpatterns = router.urls + product_router.urls + cart_router.urls


