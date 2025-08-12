from django.urls import path, include
from . import views

app_name = 'suppliers'


urlpatterns = [
    path('', views.SupplierView.as_view(), name='suppliers_view'),
    path('delete-supplier/<int:pk>/', views.DeleteSupplierView.as_view(), name='delete_supplier'),
    path('edit-supplier/<int:pk>/', views.EditSupplierView.as_view(), name='edit_supplier'),
]
