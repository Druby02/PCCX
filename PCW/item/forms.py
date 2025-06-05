from django import forms

from .models import Item, StorePrice

from django.forms import inlineformset_factory

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'base_price', "unit_type", "unit_amount", 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'base_price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'unit_type': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'unit_amount': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'base_price', "unit_type", "unit_amount", 'image', 'is_sold')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'base_price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'unit_type': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'unit_amount': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }

StorePriceFormSet = inlineformset_factory(
    Item, StorePrice,
    fields=["store", "price", "currency"],
    extra=1,
    can_delete=True
)