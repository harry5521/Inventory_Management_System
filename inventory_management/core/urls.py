from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.EmployeeLoginView.as_view(), name='employee_login'),
    path('logout/', views.EmployeeLogoutView.as_view(), name='employee_logout'),
    path('employee-dashboard/', views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('manager-dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('moderator-dashboard/', views.ModeratorDashboardView.as_view(), name='moderator_dashboard'),
]
