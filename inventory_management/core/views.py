from django.shortcuts import redirect
from django.http import HttpResponseServerError
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from .forms import EmployeeLoginForm
from .models import Employee
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from orders.models import PurchaseOrder
from suppliers.models import Supplier
from products.models import Product
from django.db.models import F

# Create your views here.

class EmployeeLoginView(FormView):
    template_name = 'core/signin.html'
    form_class = EmployeeLoginForm
    # success_url = reverse_lazy('core:employee_dashboard')

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Employee').exists():
            return reverse_lazy('core:employee_dashboard')
        elif user.groups.filter(name='Manager').exists():
            return reverse_lazy('core:manager_dashboard')
        elif user.groups.filter(name='Moderator').exists():
            return reverse_lazy('core:moderator_dashboard')
        else:
            return HttpResponseServerError("User does not authenticate to any dashboard.")

    def form_valid(self, form):
        work_email = form.cleaned_data['work_email']
        password = form.cleaned_data['password']

        
        employee = authenticate(
            request=self.request,
            work_email=work_email,
            password=password
        )

        if employee is not None:
            login(self.request, employee)
            return super().form_valid(form)
        else:
            form.add_error('work_email', 'Invalid Email or Password')
            return self.form_invalid(form)


class EmployeeDashboardView(TemplateView):
    template_name = 'core/employees_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = self.request.user.groups.all()
        context['groups'] = groups
        return context
    

class ManagerDashboardView(TemplateView):
    template_name = 'core/managers_dashboard.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_orders'] = PurchaseOrder.objects.filter(status='pending')
        context['total_orders'] = PurchaseOrder.objects.filter(status='approved')
        context['total_suppliers'] = Supplier.objects.all()
        context['total_products'] = Product.objects.all()
        context['low_stock_products'] = Product.objects.filter(stock_quantity__lte=F('reorder_level'))
        return context

class ModeratorDashboardView(TemplateView):
    template_name = 'core/moderator_dashboard.html'

    


class EmployeeLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('core:employee_login')