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
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context["item_formset"]

        if form.is_valid() and item_formset.is_valid():
            # ✅ Save the main PurchaseOrder
            self.object = form.save()

            # ✅ Attach parent to formset and save children
            item_formset.instance = self.object
            items = item_formset.save(commit=False)

            # Save new/updated items
            for item in items:
                item.save()

            # Delete removed items
            for obj in item_formset.deleted_objects:
                obj.delete()

            # ✅ Recalculate total after all items are updated/deleted
            self.object.update_total_amount()

            return super().form_valid(form)  # redirects to success_url
        else:
            # ❌ If errors, show page again with errors
            return self.form_invalid(form)
