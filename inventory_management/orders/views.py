from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView, UpdateView

# Create your views here.

class OrdersView(FormView):
    template_name = 'orders/orders.html'
    success_url = reverse_lazy('orders:orders_view')
