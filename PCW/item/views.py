from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm, StorePriceFormSet
from .models import Category, Item, Cart, CartItem
from currency_converter import CurrencyConverter
from django.contrib import messages


def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    target_currency = request.session.get("currency", "NOK")

    for item in items:
        print("Converting item:", item.name)
        item.converted_price = price_converter(item.base_price, target_currency)

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        "currency": target_currency
    })

from item.currency_utils import price_converter

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    target_currency = request.session.get("currency", "NOK")
    converted_price = price_converter(item.base_price, target_currency)

    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        "converted_price": converted_price,
        "currency": target_currency,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        formset = StorePriceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.currency_type = "NOK"
            item.created_by = request.user
            item.save()
            formset.instance = item
            formset.save()

            messages.success(request, "Item successfully created.")
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
        formset = StorePriceFormSet()

    return render(request, 'item/form.html', {
        'form': form,
        "formset": formset,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        formset = StorePriceFormSet(request.POST, instance=item)

        if form.is_valid():
            form.save()
            formset.save()

            messages.success(request, "Item successfully updated.")
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
        formset = StorePriceFormSet(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        "formset": formset,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    messages.success(request, "Item deleted.")
    return redirect('dashboard:index')


def items_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(category=category, is_sold=False)
    categories = Category.objects.all()

    return render(request, 'item/items_by_category.html', {
        'items': items,
        'category': category,
        'categories': categories
    })
@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, "Item added to cart.")
    return redirect('item:cart')

@login_required
def remove_from_cart(request, item_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('item:cart')

def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('item').all()
    cart_total = sum(entry.item.base_price * entry.quantity for entry in cart_items)

    currency = request.session.get("currency", "NOK")
    
    converted_total = cart_total
    if currency != "NOK":
        c = CurrencyConverter()
        try:
            converted_total = c.convert(cart_total, 'NOK', currency)
        except Exception:
            converted_total = cart_total 

    return render(request, 'item/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'converted_total': converted_total,
        'currency': currency,
    })

from django.contrib.auth.decorators import login_required

@login_required
def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('item:cart')

