from django import forms
from .models import Product, Category
from suppliers.models import Supplier


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'supplier', 'category', 'price', 'stock_quantity', 'reorder_level', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique SKU code'}),
            'supplier': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Supplier'}),
            'category': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Category'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Set product price'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Set stock quantity'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Set reorder value'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 9, 'placeholder': 'Enter product description'}),
        }
        labels = {
            'name': 'Product Name',
            'sku': 'SKU',
            'supplier': 'Supplier',
            'category': 'Category',
            'price': 'Price',
            'stock_quantity': 'Stock Quantity',
            'reorder_level': 'Reorder Level',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.all()
        self.fields['category'].queryset = Category.objects.all()
