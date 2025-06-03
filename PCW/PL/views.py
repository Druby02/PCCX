from django.shortcuts import render, get_object_or_404
from .models import product

def detail (request, pk):
    product = get_object_or_404(product, pk=pk)

    return render(request, 'product/detail.html', {'product': product})
