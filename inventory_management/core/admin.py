from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Department, Employee

# Register your models here.
admin.site.register(Department)


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    model = Employee
    list_display = ['id', 'full_name', 'department', 'work_email']
    list_filter = ['is_staff', 'is_active', 'groups']
    search_fields = ['full_name', 'work_email']

    ordering = ['id']

    # Add your custom fields into the fieldsets so they show in admin
    fieldsets = (
        (None, {'fields': ('work_email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'department', 'phone_no')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('work_email', 'full_name', 'department', 'phone_no', 'password1', 'password2', 'is_active', 'is_staff', 'groups', 'user_permissions'),
        }),
    )