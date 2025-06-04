from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category, Item, Cart, CartItem

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
        item.converted_price = price_converter(item.price, target_currency)

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
    converted_price = price_converter(item.price, target_currency)

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

        if form.is_valid():
            item = form.save(commit=False)
            item.currency_type = "NOK"
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

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
    return redirect('item:cart')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    if item_id_str in cart:
        del cart[item_id_str]
    request.session['cart'] = cart
    return redirect('item:cart')

def cart(request):
    cart = request.session.get('cart', {})
    items = Item.objects.filter(id__in=cart.keys())
    cart_items = []
    for item in items:
        cart_items.append({
            'item': item,
            'quantity': cart[str(item.id)]
        })
    return render(request, 'item/cart.html', {'cart_items': cart_items})

def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        item_id_str = str(item_id)
        if quantity > 0:
            cart[item_id_str] = quantity
        elif item_id_str in cart:
            del cart[item_id_str]
        request.session['cart'] = cart
    return redirect('item:cart')