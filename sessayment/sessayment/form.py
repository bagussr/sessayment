from django.http import HttpRequest, JsonResponse
from django.contrib.auth.hashers import make_password
from custom_admin.models import Account


class LoginForm:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.valid = self.is_valid()
        self.username = None
        self.password = None

    def is_valid(self):
        if self.request.POST.get("username") and self.request.POST.get("password"):
            self.username = self.request.POST.get("username")
            self.password = self.request.POST.get("password")
            return True
        return False


class RegisterForm:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.valid = self.is_valid()
        self.username = None
        self.password = None
        self.unique_id = None
        self.email = None
        self.name = None
        self.jurusan = None

    def is_valid(self):
        if (
            self.request.POST.get("username")
            and self.request.POST.get("password")
            and self.request.POST.get("unique_id")
            and self.request.POST.get("email")
            and self.request.POST.get("name")
            and self.request.POST.get("jurusan")
        ):
            self.username = self.request.POST.get("username")
            self.password = self.request.POST.get("password")
            self.unique_id = self.request.POST.get("unique_id")
            self.email = self.request.POST.get("email")
            self.name = self.request.POST.get("name")
            self.jurusan = self.request.POST.get("jurusan")
            return True
        return False

    def save(self):
        _account = Account.objects.filter(username=self.username).first()
        if _account:
            return False
        else:
            try:
                first_name, last_name = self.name.split(" ", 1)
                if len(self.unique_id) > 7:
                    _account = Account.objects.create(
                        username=self.username,
                        password=make_password(self.password),
                        unique_id=self.unique_id,
                        is_dosen=True,
                        first_name=first_name,
                        last_name=last_name,
                        jurusan=self.jurusan,
                        email=self.email,
                    )
                else:
                    _account = Account.objects.create(
                        username=self.username,
                        password=make_password(self.password),
                        unique_id=self.unique_id,
                        is_mahasiswa=True,
                        first_name=first_name,
                        last_name=last_name,
                        jurusan=self.jurusan,
                        email=self.email,
                    )
            except Exception as e:
                print(e)
                return False
            return True
