from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('', views.PurchaseOrderView.as_view(), name='orders_view')
]
