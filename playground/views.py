from django.shortcuts import render
from store.models import Product
# Create your views here.


def index(request): 
    queryset = Product.objects.filter(price__gt=100)
    context = {
        'products': queryset
    }
    return render(request, 'index.html', context)