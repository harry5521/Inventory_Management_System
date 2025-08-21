from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView, UpdateView
from .models import Product
from .forms import ProductForm
from django.db.models import Q

# Create your views here.

class ProductView(FormView):
    model = Product
    form_class = ProductForm
    template_name = 'products/products.html'
    success_url = reverse_lazy('products:products_view')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('search_product', '').strip()
        products = Product.objects.all()
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(sku__icontains=query)
            )
        
        context['products'] = products
        return context
    

class DeleteProductView(DeleteView):
    model = Product
    template_name = 'products/products.html'
    success_url = reverse_lazy('products:products_view')

class EditProductView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/products.html'
    success_url = reverse_lazy('products:products_view')

