from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from .forms import EmployeeLoginForm
from .models import Employee
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class EmployeeLoginView(FormView):
    template_name = 'core/signin.html'
    form_class = EmployeeLoginForm
    success_url = reverse_lazy('core:employee_dashboard')

    def form_valid(self, form):
        work_email = form.cleaned_data['work_email']
        department = form.cleaned_data['department']
        password = form.cleaned_data['password']

        try:
            is_employee = Employee.objects.get(work_email=work_email, department=department)
        except Employee.DoesNotExist:
            form.add_error('work_email', 'Employee not found with provided email and department.')
            return self.form_invalid(form)
        
        employee = authenticate(
            request=self.request,
            work_email=work_email,
            department=department,
            password=password,
            emp=is_employee
        )

        if employee is not None:
            login(self.request, employee)
            return super().form_valid(form)
        else:
            form.add_error('password', 'Invalid password for this email')
            return self.form_invalid(form)


class EmployeeDashboardView(TemplateView):
    template_name = 'core/dashboard.html'


class EmployeeLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('core:employee_login')