from django.urls import path
from store import views

urlpatterns = [
    # path('products/', views.product_list,name='product-list'),
    path('products/', views.product_list),
    path('products/<int:pk>/', views.product_detail),
    path('collections/<int:pk>/', views.collection_details,name='collection-details'),
    # path('collections/', views.collection_list,name='collection-list'),
    path('collections/', views.collection_list),
    path('collections/<int:pk>/', views.collection_details),
]
