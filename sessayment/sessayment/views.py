from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout
from django.http.response import HttpResponseRedirect
from django.http.request import HttpRequest

from .form import LoginForm, RegisterForm
from custom_admin.models import Account


def index(request):
    user = request.user
    if user.is_authenticated:
        if user.is_dosen:
            return redirect("dosen")
        elif user.is_mahasiswa:
            return redirect("mahasiswa")
        else:
            return redirect("admin.index")
    return render(request, "index.html")


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("index")


def restricted(request):
    return render(request, "helper/401.html")


def not_found(request):
    return render(request, "helper/404.html")


def server_error(request):
    return render(request, "helper/500.html")


class LoginView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return HttpResponseRedirect("/")
        return render(request, "auth/login.html")

    def post(self, request):
        form = LoginForm(request)
        if form.is_valid():
            account = self.auth(form.username, form.password)
            if account:
                login(request, account)
                if account.is_dosen:
                    return redirect("dosen")
                elif account.is_mahasiswa:
                    return redirect("mahasiswa")
                else:
                    return redirect("admin.index")
            return render(request, "auth/login.html", {"error": "Username atau password salah"})
        return render(request, "auth/login.html", {"error": "Pastikan semua form terisi"})

    @staticmethod
    def auth(username=None, password=None):
        if "@" in username:
            kwargs = {"email": username}
        else:
            kwargs = {"username": username}
        try:
            user = Account.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None


class RegisterView(View):
    def get(self, request):
        return render(request, "auth/register.html")

    def post(self, request):
        form = RegisterForm(request)
        if form.is_valid():
            if form.save():
                return redirect("signin")
            return render(request, "auth/register.html", {"error": "Username sudah terdaftar"})
