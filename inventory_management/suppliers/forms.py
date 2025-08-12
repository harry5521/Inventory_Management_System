from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'city', 'country', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Supplier Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact person Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone No'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Enter City Name'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Enter Country Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Enter Supplier Address'}),
        }
        labels = {
            'name': 'Supplier Name',
            'contact_person': 'Contact Person',
            'phone': 'Phone No',
            'email': 'Email',
            'city': 'City',
            'country': 'Country',
            'address': 'Address',
        }

