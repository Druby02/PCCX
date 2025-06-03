from django.urls import path

from . import views

app_name = 'PL'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail')
]