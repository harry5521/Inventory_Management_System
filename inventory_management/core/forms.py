from django import forms
from .models import Employee, Department

class EmployeeLoginForm(forms.Form):
    work_email = forms.EmailField(
        label='Work Email',
        widget=forms.EmailInput(
            attrs={'class': 'w-full h-11 px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
            'placeholder':'Enter your work email'
            }
        )
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'w-full h-11 px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
            'placeholder':'Enter your password'
            }
        )
    )


    def clean_work_email(self):
        value = self.cleaned_data.get('work_email')
        if not value.endswith('@inventoryemp.com'):
            raise forms.ValidationError("Please use your valid work email.")
        return value