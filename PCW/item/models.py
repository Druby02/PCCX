from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

def default_expiry():
    return timezone.now() + timedelta(days=15)

class Category(models.Model):
    name = models.CharField(max_length=100,)

    class Meta:
        ordering = ['name',]
        verbose_name_plural = 'Categories' 

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='items_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    expires_at = models.DateTimeField(default=default_expiry, blank=True, null=True)

    class Meta:
        ordering = ['name',]
        verbose_name_plural = 'items'

    def __str__(self):
        return self.name