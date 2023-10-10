from django.shortcuts import render
from django.views.generic import View
from django.http.request import HttpRequest
from django.http.response import JsonResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import MataKuliah, Account
from .form import AddMatakuliahForm, AddDosenForm, EditDosenForm, AddMahasiswaForm


# Create your views here.
@login_required(login_url="../signin/")
@permission_required("is_superuser", login_url="../signin/")
def index(request):
    return render(request, "admin/index.html")


@login_required(login_url="../signin/")
@permission_required("is_superuser", login_url="../signin/")
def delete_user(request, _id):
    user = Account.objects.get(id=_id)
    user.delete()
    return HttpResponseRedirect("/admin/dosen/")


@method_decorator(login_required(login_url="../signin/"), name="dispatch")
@method_decorator(permission_required("is_superuser", login_url="../signin/"), name="dispatch")
class AdminDosenView(View):
    def get(self, request):
        dosen = Account.objects.filter(is_dosen=True).order_by("id")
        return render(request, "admin/dosen.html", {"dosen": dosen})

    def post(self, request):
        form = AddDosenForm(request)
        if form.is_valid():
            form.save()
            dosen = Account.objects.filter(is_dosen=True)
            return render(request, "admin/dosen.html", {"dosen": dosen})
        return render(request, "admin/dosen.html", {"error": "Pastikan semua form terisi"})

    @staticmethod
    @csrf_exempt
    def patch(request: HttpRequest):
        if request.method == "POST":
            form = EditDosenForm(request)
            if form.is_valid():
                form.save()
                return JsonResponse({"status": "ok", "code": 200})
            return JsonResponse({"status": "error", "code": 400})
        return HttpResponseNotAllowed(["POST"])

    @staticmethod
    def detail(request: HttpRequest, _id):
        dosen = Account.objects.get(id=_id)
        return JsonResponse(
            {
                "id": dosen.id,
                "username": dosen.username,
                "name": dosen.first_name + " " + dosen.last_name,
                "email": dosen.email,
                "unique_id": dosen.unique_id,
                "jurusan": dosen.jurusan,
                "is_mahasiswa": dosen.is_mahasiswa,
                "is_dosen": dosen.is_dosen,
                "is_superuser": dosen.is_superuser,
                "is_staff": dosen.is_staff,
                "is_active": dosen.is_active,
            }
        )


class AdminMahasiswaView(View):
    def get(self, request):
        mahasiswa = Account.objects.filter(is_mahasiswa=True)
        return render(request, "admin/mahasiswa.html", {"mahasiswa": mahasiswa})

    def post(self, request):
        form = AddMahasiswaForm(request)
        mahasiswa = Account.objects.filter(is_mahasiswa=True)
        if form.is_valid():
            form.save()
            return render(request, "admin/mahasiswa.html", {"mahasiswa": mahasiswa})
        return render(request, "admin/mahasiswa.html", {"error": "Pastikan semua form terisi", "mahasiswa": mahasiswa})


class AdminMataKuliahView(View):
    def get(self, request):
        matkul = MataKuliah.objects.all()
        return render(request, "admin/matakuliah.html", {"matkul": matkul})

    def post(self, request):
        form = AddMatakuliahForm(request)
        if form.is_valid():
            x = form.save()
            matkul = MataKuliah.objects.all()
            return render(request, "admin/matakuliah.html", {"matkul": matkul})
        return render(request, "admin/matakuliah.html", {"error": "Pastikan semua form terisi"})
