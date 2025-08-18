from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from .forms import PurchaseOrderForm, PurchaseOrderItemFormSet
from .models import PurchaseOrder, PurchaseOrderItem

# Create your views here.

class ListPurchaseOrdersView(ListView):
    model = PurchaseOrder
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return PurchaseOrder.objects.prefetch_related('items')
    
class DeletePurchaseOrderView(DeleteView):
    model = PurchaseOrder
    template_name = 'orders/orders_list.html'
    success_url = reverse_lazy('orders:orders_view')


class CreatePurchaseOrderView(CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'orders/CreateUpdate_orders.html'
    success_url = reverse_lazy('orders:orders_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = PurchaseOrderItemFormSet(self.request.POST)
        else:
            context['item_formset'] = PurchaseOrderItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        self.object = form.save()
        if item_formset.is_valid():
            item_formset.instance = self.object
            item_formset.save()
            self.object.update_total_amount()  # Update total amount after saving items
            return super().form_valid(form)   # ✅ go to success_url
        else:
            return self.form_invalid(form)  


class PurchaseOrderUpdateView(UpdateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = "orders/CreateUpdate_orders.html"
    success_url = reverse_lazy("orders:orders_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["item_formset"] = PurchaseOrderItemFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context["item_formset"] = PurchaseOrderItemFormSet(instance=self.object)
        print(f'context = {context}')
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context["item_formset"]

        # self.object must be set first
        self.object = form.save(commit=False)

        if item_formset.is_valid():
            self.object.save()  # ✅ save parent
            item_formset.instance = self.object
            self.object = form.save()  # save again with relations

            # Save children
            items = item_formset.save(commit=False)
            for item in items:
                item.save()
            for obj in item_formset.deleted_objects:
                obj.delete()

            # update total
            self.object.update_total_amount()
            return super().form_valid(form)
        
        print("Form errors:", form.errors)
        print("Formset errors:", item_formset.errors)
        print("Formset non-form errors:", item_formset.non_form_errors())
        return self.form_invalid(form)  # ✅ go to form_invalid