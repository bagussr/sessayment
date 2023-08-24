from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponseRedirect
from django.views.generic import View
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from .form import AddScheduleForm, AddQuestionForm
from .models import Assesment, AssesmentQuestion, Question, Skors

from custom_admin.models import MataKuliah


def custom_permission_dosen(role, login_url=None, raise_exception=False):
    def check_role(user):
        if user.is_dosen == role and user.is_staff == role:
            return True
        if raise_exception:
            raise PermissionDenied
        return False

    return user_passes_test(check_role, login_url=login_url)


# Create your views here.
@login_required(login_url="../signin/")
@custom_permission_dosen(role=True, raise_exception=True)
def schedule(request):
    assesment = Assesment.objects.all()
    for i in assesment:
        i.jenis_ujian = i.get_jenis_ujian()
    return render(request, "dosen/schedule/index.html", {"assesment": assesment})


@login_required(login_url="../signin/")
@custom_permission_dosen(role=True, raise_exception=True)
def schedule_action(request, id):
    assesment = Assesment.objects.get(id=id)
    return render(request, "dosen/schedule/action.html", {"assesment": assesment})


@login_required(login_url="../signin/")
@custom_permission_dosen(role=True, raise_exception=True)
def assesment(request, id):
    soal = 0
    assesment = Assesment.objects.get(id=id)
    assesment_question = AssesmentQuestion.objects.filter(assesment=assesment).first()
    if assesment_question:
        question = Question.objects.filter(assement_question=assesment_question)
        for i in question:
            soal += 1
        return render(request, "dosen/assesment.html", {"soal": soal, "poin": assesment_question.poin, "id": id})
    else:
        try:
            assesment_question = AssesmentQuestion.objects.create(assesment=assesment, poin=0, created_by=request.user)
            question = Question.objects.filter(assement_question=assesment_question)
            for i in question:
                soal += 1
            return render(request, "dosen/assesment.html", {"soal": soal, "poin": assesment_question.poin, "id": id})
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)})


@login_required(login_url="../signin/")
@custom_permission_dosen(role=True, raise_exception=True)
def score(request, id):
    assesment = Assesment.objects.get(id=id)
    skor = Skors.objects.filter(assesment=assesment)
    return render(request, "dosen/schedule/score.html", {"assesment": assesment, "skor": skor})


@method_decorator(login_required(login_url="../signin/"), name="dispatch")
@method_decorator(custom_permission_dosen(role=True, raise_exception=True), name="dispatch")
class ScheduleAddView(View):
    def get(self, request):
        matkul = MataKuliah.objects.all()
        return render(request, "dosen/schedule/add.html", {"matkul": matkul})

    def post(self, request):
        form = AddScheduleForm(request)
        if form.is_valid():
            form.save()
            return redirect("dosen")
        return render(request, "dosen/schedule/add.html", {"error": "Pastikan semua form terisi"})


@method_decorator(login_required(login_url="../signin/"), name="dispatch")
@method_decorator(custom_permission_dosen(role=True, raise_exception=True), name="dispatch")
class ScheduleEditView(View):
    def get(self, request, id):
        matkul = MataKuliah.objects.all()
        assesment = Assesment.objects.get(id=id)
        return render(request, "dosen/schedule/edit.html", {"mata_kuliah": matkul, "assesment": assesment})

    def post(self, request, id):
        form = AddScheduleForm(request)
        if form.is_valid():
            assesment = Assesment.objects.get(id=id)
            assesment.mata_kuliah = MataKuliah.objects.get(id=form.mata_kuliah)
            assesment.jenis_ujian = form.jenis_ujian
            assesment.tanggal = form.tanggal
            assesment.waktu_mulai = form.waktu_mulai
            assesment.waktu_selesai = form.waktu_selesai
            assesment.save()
            return redirect("dosen")

    @staticmethod
    def delete(request, id):
        assesment = Assesment.objects.get(id=id)
        assesment.delete()
        return redirect("dosen")


@method_decorator(login_required(login_url="../signin/"), name="dispatch")
@method_decorator(custom_permission_dosen(role=True, raise_exception=True), name="dispatch")
class QuestionAddView(View):
    def get(self, request, id):
        assesment = Assesment.objects.get(id=id)
        if self.check_assesment_question(assesment):
            assesment_question = AssesmentQuestion.objects.get(assesment=assesment)
            question = Question.objects.filter(assement_question=assesment_question)
            return render(request, "dosen/add_question.html", {"assesment": assesment, "question": question})
        try:
            AssesmentQuestion.objects.create(assesment=assesment, poin=0, created_by=request.user)
            return render(request, "dosen/add_question.html", {"assesment": assesment})
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)})

    def post(self, request, id):
        form = AddQuestionForm(request)
        if form.is_valid():
            form.save(id)
            assesment = Assesment.objects.get(id=id)
            assesment_question = AssesmentQuestion.objects.get(assesment=assesment)
            question = Question.objects.filter(assement_question=assesment_question)
            return render(request, "dosen/add_question.html", {"assesment": assesment, "question": question})
        return render(request, "dosen/add_question.html", {"error": "Pastikan semua form terisi"})

    @staticmethod
    def edit(request, id):
        _id = request.POST.get("id")
        soal = request.POST.get("soal")
        jawaban = request.POST.get("jawaban_a")
        point = request.POST.get("point")
        question = Question.objects.get(id=_id)
        question.soal = soal
        question.jawaban_a = jawaban
        question.poin = point
        question.save()
        return redirect("schedule.add.question", id=id)

    @staticmethod
    def delete(request, id, question_id):
        question = Question.objects.get(id=question_id)
        question.delete()
        return HttpResponseRedirect("/")

    @staticmethod
    def detail(request, id, question_id):
        x = request.GET.get("id")
        question = Question.objects.get(id=x)
        return JsonResponse({"question": model_to_dict(question)})

    @staticmethod
    def check_assesment_question(assesment):
        question = AssesmentQuestion.objects.filter(assesment=assesment)
        if question:
            return True
        return False
