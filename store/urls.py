from django.urls import path
from rest_framework_nested import routers
from store import views

router = routers.DefaultRouter()

router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

product_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_routers.register('reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls + product_routers.urls
