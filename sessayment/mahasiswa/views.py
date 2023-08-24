from django.shortcuts import render, redirect
from django.views.generic import View
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

from datetime import datetime

from .models import MahasiswaAssesment
from dosen.models import Assesment, AssesmentQuestion, Question, Skors


# function to convert datetime.time to minutes
def time_to_minute(time):
    return time.hour * 60 + time.minute


def custom_permission_mahasiswa(role, login_url=None, raise_exception=False):
    def check_role(user):
        if user.is_mahasiswa == role:
            return True
        if raise_exception:
            raise PermissionDenied
        return False

    return user_passes_test(check_role, login_url=login_url)


# Create your views here.
@method_decorator(login_required(login_url="../signin/"), name="dispatch")
@method_decorator(custom_permission_mahasiswa(role=True, raise_exception=True), name="dispatch")
class MahasiswaView(View):
    def get(self, request: HttpRequest):
        assesment = Assesment.objects.all()
        for i in assesment:
            i.jenis_ujian = i.get_jenis_ujian()
        return render(request, "mahasiswa/schedule.html", {"assesment": assesment})


@method_decorator(login_required(login_url="../../signin/"), name="dispatch")
@method_decorator(custom_permission_mahasiswa(role=True, raise_exception=True), name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class MahasiswaAssesmentView(View):
    def get(self, request: HttpRequest, id):
        start_time = None
        if self.get_headers(request):
            assesment = Assesment.objects.get(id=id)
            assesment_question = AssesmentQuestion.objects.filter(assesment=assesment).first()
            question = Question.objects.filter(assement_question=assesment_question)
            mahasiswa_assesment = MahasiswaAssesment.objects.filter(mahasiswa=request.user, assesment=assesment).first()
            return JsonResponse(
                {
                    "status": "success",
                    "data": {
                        "assesment": model_to_dict(assesment),
                        "question": [model_to_dict(i, exclude=["jawaban", "poin"]) for i in question]
                        if question
                        else None,  # noqa: E501
                        "mahasiswa_assesment": model_to_dict(mahasiswa_assesment) if mahasiswa_assesment else None,
                    },
                }
            )
        else:
            assesment = Assesment.objects.get(id=id)
            if datetime.now().date() > assesment.tanggal or datetime.now().time() > assesment.waktu_selesai:
                return render(request, "helper/assesment_error.html", {"error": "Waktu ujian telah berakhir"})
            if datetime.now().date() < assesment.tanggal and datetime.now().time() < assesment.waktu_mulai:
                return render(request, "helper/assesment_error.html", {"error": "Waktu ujian belum dimulai"})
            assesment_question = AssesmentQuestion.objects.filter(assesment=assesment).first()
            len_question = Question.objects.filter(assement_question=assesment_question).count()
            mahasiswa = MahasiswaAssesment.objects.filter(mahasiswa=request.user, assesment=assesment).first()
            if not mahasiswa:
                mahasiswa = MahasiswaAssesment.objects.create(mahasiswa=request.user, assesment=assesment)
                start_time = mahasiswa.created_at.astimezone(datetime.now().astimezone().tzinfo)
            start_time = mahasiswa.created_at.astimezone(datetime.now().astimezone().tzinfo)
            time_assesment = time_to_minute(assesment.waktu_selesai) - time_to_minute(assesment.waktu_mulai)
            return render(
                request,
                "mahasiswa/assesment.html",
                {
                    "assesment": assesment,
                    "assesment_question": assesment_question,
                    "time_assesment": time_assesment,
                    "start_time": start_time,
                    "len_question": len_question,
                },
            )

    def post(self, request: HttpRequest, id):
        assesment = Assesment.objects.get(id=id)
        jawaban = request.POST.get("jawaban")
        # Skors.objects.create(mahasiswa=request.user, assesment=assesment, skor=100)
        return JsonResponse({"status": "success", "url": redirect("mahasiswa.result", id=id).url})

    @staticmethod
    def get_headers(request: HttpRequest):
        if (
            request.headers.get("Content-Type") == "application/json"
            and request.headers.get("Accept") == "application/json"
        ):
            return True
        return False


@method_decorator(login_required(login_url="../../signin/"), name="dispatch")
@method_decorator(custom_permission_mahasiswa(role=True, raise_exception=True), name="dispatch")
class MahasiswaTermsView(View):
    def get(self, request: HttpRequest, id):
        assesment = Assesment.objects.get(id=id)
        return render(request, "mahasiswa/terms.html", {"id": id, "assesment": assesment})


@method_decorator(login_required(login_url="../../signin/"), name="dispatch")
@method_decorator(custom_permission_mahasiswa(role=True, raise_exception=True), name="dispatch")
class MahasiswaResultView(View):
    def get(self, request: HttpRequest, id):
        assesment = Assesment.objects.get(id=id)
        # score = Skors.objects.filter(mahasiswa=request.user, assesment=assesment).first()
        return render(request, "mahasiswa/result.html")
