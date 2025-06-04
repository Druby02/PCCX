from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm
from .views import set_currency

from django.contrib.auth.views import LogoutView

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path("set_currency/", views.set_currency, name="set_currency")
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='core:index'), name='logout'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),


]
