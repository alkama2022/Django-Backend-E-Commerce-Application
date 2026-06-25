
from rest_framework_nested import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()

router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

product_router = routers.NestedDefaultRouter(router,'products', lookup='product') # parents router

product_router.register('reviews',views.ReviewViewSet,basename='product_reviews') #Chield Router

urlpatterns = router.urls + product_router.urls


