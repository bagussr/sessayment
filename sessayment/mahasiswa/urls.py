from django.urls import path

from .views import MahasiswaView, MahasiswaAssesmentView, MahasiswaTermsView, MahasiswaResultView

urlpatterns = [
    path("", MahasiswaView.as_view(), name="mahasiswa"),
    path("assesment/<int:id>", MahasiswaAssesmentView.as_view(), name="mahasiswa.assesment"),
    path("terms/<int:id>", MahasiswaTermsView.as_view(), name="mahasiswa.terms"),
    path("result/<int:id>", MahasiswaResultView.as_view(), name="mahasiswa.result"),
]
