from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class DuberUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, phone_number, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, phone_number, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
            password=password
        )

        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


# Create your models here.
class DuberUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']

    objects = DuberUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class DuberDriver(models.Model):
    class VehicleType(models.IntegerChoices):
        DuberX = 1
        DuberXL = 2
        DuberComfort = 3

    duber_user = models.ForeignKey(DuberUser, on_delete=models.CASCADE, to_field='username')
    vehicle_type = models.IntegerField(choices=VehicleType, default=VehicleType.DuberX)
    licence_plate_number = models.CharField(max_length=50)
    special_info = models.TextField()
