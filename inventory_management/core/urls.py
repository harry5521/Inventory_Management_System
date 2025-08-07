from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.EmployeeLoginView.as_view(), name='employee_login'),
    path('logout/', views.EmployeeLogoutView.as_view(), name='employee_logout'),
    path('dashboard/', views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
]
