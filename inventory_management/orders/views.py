from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views import View
from .forms import PurchaseOrderForm, PurchaseOrderItemFormSet
from .models import PurchaseOrder, PurchaseOrderItem

# Create your views here.

class PurchaseOrderView(View):
    def get(self, request):
        order_form = PurchaseOrderForm()
        formset = PurchaseOrderItemFormSet()
        orders = PurchaseOrder.objects.all()
        return render(request, 'orders/orders.html', {
            'order_form': order_form,
            'formset': formset,
            'orders': orders
        })

    def post(self, request):
        order_form = PurchaseOrderForm(request.POST)
        formset = PurchaseOrderItemFormSet(request.POST)

        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.created_by = request.user
            order.save()

            # Link each item to the new order
            items = formset.save(commit=False)
            for item in items:
                item.order = order
                item.save()

            order.update_total_amount()
            return redirect('orders:orders_view')

        return render(request, 'orders/orders.html', {
            'order_form': order_form,
            'formset': formset
        })