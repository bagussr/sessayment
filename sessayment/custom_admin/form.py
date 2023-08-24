from django.http.request import HttpRequest
from django.contrib.auth.hashers import make_password

from .models import MataKuliah, Account


class AddMahasiswaForm:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.name = None
        self.email = None
        self.jurusan = None
        self.unique_id = None

    def is_valid(self):
        if (
            self.request.POST.get("name")
            and self.request.POST.get("email")
            and self.request.POST.get("jurusan")
            and self.request.POST.get("nim")
        ):
            self.name = self.request.POST.get("name")
            self.email = self.request.POST.get("email")
            self.jurusan = self.request.POST.get("jurusan")
            self.unique_id = self.request.POST.get("nim")
            return True

    def save(self):
        try:
            first_name, last_name = self.name.split(" ", 1) if len(self.name.split()) > 1 else (self.name, "")
            Account.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=self.email,
                jurusan=self.jurusan,
                unique_id=self.unique_id,
                is_mahasiswa=True,
                password=make_password("mahasiswa123"),
            )
            return True
        except Exception as e:
            print(e)
            return False


class AddMatakuliahForm:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.name = None

    def is_valid(self):
        if self.request.POST.get("name"):
            self.name = self.request.POST.get("name")
            return True
        return False

    def save(self):
        try:
            MataKuliah.objects.create(name=self.name)
            return True
        except Exception as e:
            print(e)
            return False


class AddDosenForm:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.name = None
        self.email = None
        self.jurusan = None
        self.unique_id = None

    def is_valid(self):
        if (
            self.request.POST.get("name")
            and self.request.POST.get("email")
            and self.request.POST.get("jurusan")
            and self.request.POST.get("nim")
        ):
            self.name = self.request.POST.get("name")
            self.email = self.request.POST.get("email")
            self.jurusan = self.request.POST.get("jurusan")
            self.unique_id = self.request.POST.get("nim")
            return True
        return False

    def save(self):
        try:
            first_name, last_name = self.name.split(" ", 1) if len(self.name.split()) > 1 else (self.name, "")
            Account.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=self.email,
                jurusan=self.jurusan,
                unique_id=self.unique_id,
                is_dosen=True,
                password=make_password("dosen123"),
            )
            return True
        except Exception as e:
            print(e)
            return False


class EditDosenForm:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.name = None
        self.nim = None
        self.email = None
        self.jurusan = None
        self.is_staff = None
        self.id = None

    def is_valid(self):
        if (
            self.request.POST.get("name")
            and self.request.POST.get("nim")
            and self.request.POST.get("email")
            and self.request.POST.get("jurusan")
            and self.request.POST.get("is_staff")
            and self.request.POST.get("id")
        ):
            self.name = self.request.POST.get("name")
            self.nim = self.request.POST.get("nim")
            self.email = self.request.POST.get("email")
            self.jurusan = self.request.POST.get("jurusan")
            self.is_staff = self.request.POST.get("is_staff")
            self.id = self.request.POST.get("id")
            return True

    def save(self):
        account = Account.objects.get(id=self.id)
        try:
            account.first_name, account.last_name = (
                self.name.split(" ", 1) if len(self.name.split()) > 1 else (self.name, "")
            )
            account.email = self.email
            account.jurusan = self.jurusan
            account.unique_id = self.nim
            account.is_staff = True if self.is_staff == "true" else False
            account.save()
            return True
        except Exception as e:
            print(e)
            return False
