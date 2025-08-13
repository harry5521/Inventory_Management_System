from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('', views.OrdersView.as_view(), name='orders_view')
]
