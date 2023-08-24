from django.http.request import HttpRequest

from custom_admin.models import MataKuliah
from .models import Assesment, Question, AssesmentQuestion


class AddScheduleForm:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.mata_kuliah = None
        self.jenis_ujian = None
        self.tanggal = None
        self.waktu_mulai = None
        self.waktu_selesai = None
        self.created_by = None

    def is_valid(self):
        if (
            self.request.POST.get("matkul")
            and self.request.POST.get("ujian")
            and self.request.POST.get("tanggal")
            and self.request.POST.get("starttime")
            and self.request.POST.get("endtime")
        ):
            self.mata_kuliah = self.request.POST.get("matkul")
            self.jenis_ujian = self.request.POST.get("ujian")
            self.tanggal = self.request.POST.get("tanggal")
            self.waktu_mulai = self.request.POST.get("starttime")
            self.waktu_selesai = self.request.POST.get("endtime")
            self.created_by = self.request.user
            return True
        return False

    def save(self):
        try:
            Assesment.objects.create(
                mata_kuliah=MataKuliah.objects.get(id=self.mata_kuliah),
                jenis_ujian=self.jenis_ujian,
                tanggal=self.tanggal,
                waktu_mulai=self.waktu_mulai,
                waktu_selesai=self.waktu_selesai,
                created_by=self.created_by,
            )
            return True
        except Exception as e:
            print(e)
            return False


class AddQuestionForm:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.soal = None
        self.jawaban = None
        self.poin = None
        self.created_by = None

    def is_valid(self):
        if self.request.POST.get("soal") and self.request.POST.get("kunci") and self.request.POST.get("point"):
            self.soal = self.request.POST.get("soal")
            self.jawaban = self.request.POST.get("kunci")
            self.poin = self.request.POST.get("point")
            self.created_by = self.request.user
            return True
        return False

    def save(self, id):
        assesment = Assesment.objects.get(id=id)
        assesment_question = AssesmentQuestion.objects.get(assesment=assesment)
        try:
            Question.objects.create(
                assement_question=assesment_question,
                soal=self.soal,
                jawaban=self.jawaban,
                poin=self.poin,
            )
            return True
        except Exception as e:
            print(e)
            return False
