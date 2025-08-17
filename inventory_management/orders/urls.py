from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('', views.ListPurchaseOrdersView.as_view(), name='orders_view'),
    path('create-order/', views.CreatePurchaseOrderView.as_view(), name='create_order'),
    path('delete-order/<int:pk>/', views.DeletePurchaseOrderView.as_view(), name='delete_order'),
    path('update-order/<int:pk>/', views.PurchaseOrderUpdateView.as_view(), name='update_order')
]
