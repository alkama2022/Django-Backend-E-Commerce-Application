from rest_framework.routers import DefaultRouter
from django.urls import path
from store import views


router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls
