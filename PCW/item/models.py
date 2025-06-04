from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    

Units = [("PU", "Per Unit"),("kg", "kilogram"), ("g", "gram"), ("lb", "pound"), ("oz", "ounce"),
         ("L", "Liter"), ("ml", "milliliter"), ("gal", "gallon"), ("qt", "quart"), ("pt", "pint"),
         ("m", "meter"), ("cm", "centimeter"), ("mm", "millimeter"), ("ft", "feet"), ("in", "inch")]


class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    currency_type = models.CharField(max_length=3, default="NOK")
    unit_type= models.CharField(choices=Units, max_length=20, default="PU")
    unit_amount= models.FloatField(default=1)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in cart {self.cart.id}"
