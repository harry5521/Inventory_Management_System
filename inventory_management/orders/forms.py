from django import forms
from django.forms import inlineformset_factory
from suppliers.models import Supplier
from products.models import Product
from .models import PurchaseOrder, PurchaseOrderItem


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['order_number', 'supplier', 'payment_method', 'notes']
        widgets = {
            'order_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Order Number'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter Notes'}),
        }
        labels = {
            'order_number': 'Order Number',
            'supplier': 'Supplier',
            'payment_method': 'Payment Method',
            'notes': 'Notes',
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['supplier'].queryset = Supplier.objects.all()


class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity'}),
        }
        labels = {
            'product': 'Product',
            'quantity': 'Quantity',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()


PurchaseOrderItemFormSet = inlineformset_factory(
    parent_model=PurchaseOrder,
    model=PurchaseOrderItem,
    form=PurchaseOrderItemForm,
    extra=1,
    can_delete=True,
    validate_min=True,
    min_num=1,
)
