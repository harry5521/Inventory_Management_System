from django.urls import path, include
from . import views
from orders.views import order_approved, order_canceled


app_name = 'core'

urlpatterns = [
    path('', views.EmployeeLoginView.as_view(), name='employee_login'),
    path('logout/', views.EmployeeLogoutView.as_view(), name='employee_logout'),

    # dashboards urls
    path('employee-dashboard/', views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('manager-dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('moderator-dashboard/', views.ModeratorDashboardView.as_view(), name='moderator_dashboard'),

    # Manager related urls
    path('manager-dashboard/approved-order/<int:pk>/', order_approved, name='order_approved'),
    path('manager-dashboard/canceled-order/<int:pk>', order_canceled, name='order_canceled'),
]
