from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("Номер телефоня обязателен!")
        phone = self.normalize_phone(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone=phone, password=password, **extra_fields)
    
    def normalize_phone(self, phone: str):
        return phone.replace(' ', '').replace('+', '')


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=12, verbose_name="Номер телефона", unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="ФИО")
    email = models.EmailField("Почта", null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to="profiles/", 
        null=True, 
        blank=True,
        verbose_name="Фото",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone
