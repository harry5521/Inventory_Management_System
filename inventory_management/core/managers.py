from django.contrib.auth.base_user import BaseUserManager


class EmployeeManager(BaseUserManager):
    def create_user(self, work_email, password=None, **extra_fields):
        if not work_email:
            raise ValueError("The Email field required.")
        work_email = self.normalize_email(work_email)
        user = self.model(work_email=work_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, work_email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(work_email, password, **extra_fields)