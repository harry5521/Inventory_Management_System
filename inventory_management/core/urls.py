from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('login/', views.EmployeeLoginView.as_view(), name='employee_login'),
    path('dashboard/', views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
]
