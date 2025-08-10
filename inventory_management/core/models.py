from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import EmployeeManager

# Create your models here.

class Department(models.Model):
    dep_id = models.CharField(max_length=10, primary_key=True)
    dep_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dep_name
    
# class Role(models.Model):
#     role_id = models.CharField(max_length=10, primary_key=True)
#     role_name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.role_name

class Employee(AbstractUser):
    # Additional fields can be added here if needed
    full_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='employees_department')
    work_email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    # password = models.CharField(max_length=128)
    # role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True, related_name='employees_role')

    username = None
    USERNAME_FIELD = 'work_email'
    REQUIRED_FIELDS = []

    objects = EmployeeManager()

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['full_name']
        
    def __str__(self):
        return f"{self.full_name}"