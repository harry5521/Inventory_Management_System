from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView, UpdateView
from .models import Supplier
from .forms import SupplierForm

# Create your views here.

class SupplierView(FormView):
    template_name = 'suppliers/suppliers.html'
    form_class = SupplierForm
    success_url = reverse_lazy('suppliers:suppliers_view')

    def form_valid(self, form):
        supplier = form.save(commit=False)
        supplier.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        return context
    

class DeleteSupplierView(DeleteView):
    model = Supplier
    template_name = 'suppliers/suppliers.html'
    success_url = reverse_lazy('suppliers:suppliers_view')

class EditSupplierView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/suppliers.html'
    success_url = reverse_lazy('suppliers:suppliers_view')
