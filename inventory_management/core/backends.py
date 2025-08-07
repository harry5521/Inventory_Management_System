from django.contrib.auth.backends import ModelBackend
from .models import Employee

class EmployeeAuthBackend(ModelBackend):
    def authenticate(self, request, work_email=None, department=None, password=None, emp=None, **kwargs):
        try:
            # employee = Employee.objects.get(work_email=work_email, department=department)
            employee = emp
            # if employee.check_password(password):
            if employee.password == password:
                return employee        
        except Employee.DoesNotExist:
            return None
        