from django.urls import path, include
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.ProductView.as_view(), name='products_view'),
    path('delete-product/<int:pk>/', views.DeleteProductView.as_view(), name='delete_product'),
    path('edit-product/<int:pk>/', views.EditProductView.as_view(), name='edit_product'),
]
