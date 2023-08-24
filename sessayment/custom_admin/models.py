from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        try:
            x = Account.objects.filter(username=username).first()
        except x:
            raise ValueError("Username alreadu used")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.staff = True
        user.admin = True
        return user


# Create your models here.
class Account(AbstractUser):
    email = models.EmailField("email")
    username = models.CharField("username", max_length=250, unique=True, blank=True, null=True)
    password = models.CharField("password", max_length=100)
    unique_id = models.CharField("unique_id", max_length=25, unique=True)
    jurusan = models.CharField("jurusan", max_length=100)
    is_mahasiswa = models.BooleanField(default=False)
    is_dosen = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


object = UserManager()

USERNAME_FIELD = ["username", "email"]
REQUIRED_FIELDS = ["email"]


def to_dict(self):
    return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "unique_id": self.unique_id,
        "jurusan": self.jurusan,
        "is_mahasiswa": self.is_mahasiswa,
        "is_dosen": self.is_dosen,
        "is_superuser": self.is_superuser,
        "is_staff": self.is_staff,
        "is_active": self.is_active,
    }


def __str__(self) -> str:
    return self.username


def has_perm(self, perm, obj=None):
    return True


def has_module_perms(self, app_label):
    return True


@property
def is_staff(self):
    return self.staff


@property
def is_admin(self):
    return self.admin


@property
def name(self):
    return self.first_name + " " + self.last_name


class MataKuliah(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
