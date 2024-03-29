from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, date_of_birth, password, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            date_of_birth=date_of_birth,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, date_of_birth, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, date_of_birth, password, **extra_fields)

    def create_superuser(self, email, name, date_of_birth, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValidationError({'error_message': 'Superuser must have is_staff=True'})
        if extra_fields.get('is_superuser') is not True:
            raise ValidationError({'error_message': 'Superuser must have is_superuser=True'})

        return self._create_user(email, name, date_of_birth, password, **extra_fields)


class UserAccount(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, unique=True)
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name', 'date_of_birth')

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __repr__(self):
        return self.email
