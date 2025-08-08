from django.contrib.auth.backends import ModelBackend
from .models import Employee

class EmployeeAuthBackend(ModelBackend):
    def authenticate(self, request, employee=None, password=None, **kwargs):
        if employee.work_email and employee.department is None:
            return None
            try:
                emp = Employee.objects.get(work_email=work_email)
            except Employee.DoesNotExist:
                return None
        try:
            
            # if employee.check_password(password):
            if employee.password == password:
                return employee        
        except Employee.DoesNotExist:
            return None
        