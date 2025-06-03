from django.shortcuts import render
from django.utils import timezone

from PL.models import Product, Category
# Create your views here.
def index(request):
    products = Product.objects.filter(expires_at__gt=timezone.now())[0:6] 
    categories = Category.objects.all()

    return render(request, 'core/index.html',{
        'products': products,
        'categories': categories,
    })


def contact(request):
    return render(request, 'core/contact.html')