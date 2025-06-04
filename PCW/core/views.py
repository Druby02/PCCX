from django.shortcuts import render, redirect, get_object_or_404

from item.models import Category, Item

from .forms import SignupForm

from .forms import CurrencyForm


from .forms import EditProfileForm


def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

def about(request):
    return render(request, 'core/about.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def terms(request):
    return render(request, 'core/terms.html')

def set_currency(request):
    if request.method == "POST":
        form = CurrencyForm(request.POST)

        if form.is_valid():
            request.session["currency"] = form.cleaned_data["currency"]
            return redirect(request.META.get("HTTP_REFERER", "/"))

    return redirect("/")




from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'core/profile.html', {
        'user': request.user
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('core:profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form})

from django.contrib.auth import get_user_model, logout

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('core:index')
    return render(request, 'core/delete_profile.html')


