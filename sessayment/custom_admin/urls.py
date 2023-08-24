from django.urls import path

from .views import index, AdminDosenView, AdminMahasiswaView, AdminMataKuliahView, delete_user

urlpatterns = [
    path("", index, name="admin.index"),
    path("dosen/", AdminDosenView.as_view(), name="admin.dosen"),
    path("dosen/detail/<int:_id>", AdminDosenView.detail, name="admin.dosen.detail"),
    path("dosen/delete/<int:_id>", delete_user, name="admin.dosen.delete"),
    path("dosen/edit", AdminDosenView.patch, name="admin.dosen.edit"),
    path("mahasiswa/", AdminMahasiswaView.as_view(), name="admin.mahasiswa"),
    path("matakuliah/", AdminMataKuliahView.as_view(), name="admin.matakuliah"),
]
