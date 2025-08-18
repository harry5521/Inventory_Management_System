from django.urls import path
from .views import ListPurchaseOrdersView, CreatePurchaseOrderView, DeletePurchaseOrderView, PurchaseOrderUpdateView


app_name = 'orders'

urlpatterns = [
    # Orders URLs for Managers
    path('', ListPurchaseOrdersView.as_view(), name='orders_view'),
    path('create-order/', CreatePurchaseOrderView.as_view(), name='create_order'),
    path('delete-order/<int:pk>/', DeletePurchaseOrderView.as_view(), name='delete_order'),
    path('update-order/<int:pk>/', PurchaseOrderUpdateView.as_view(), name='update_order'),

    # Create Order url for employee
    path('create-new-order/', CreatePurchaseOrderView.as_view(), name='create_order_employee')
]
