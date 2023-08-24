from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.


class Assesment(models.Model):
    UJIAN = (
        (1, "UTS"),
        (2, "UAS"),
        (3, "Kuis"),
    )
    mata_kuliah = models.ForeignKey("custom_admin.MataKuliah", on_delete=models.CASCADE)
    jenis_ujian = models.BigIntegerField(choices=UJIAN)
    tanggal = models.DateField()
    waktu_mulai = models.TimeField()
    waktu_selesai = models.TimeField()
    created_by = models.ForeignKey("custom_admin.Account", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.mata_kuliah} - {self.jenis_ujian} - {self.tanggal} - {self.waktu_mulai} - {self.waktu_selesai}"

    def get_jenis_ujian(self):
        UJIAN = self.UJIAN
        return UJIAN[self.jenis_ujian - 1][1]


class AssesmentQuestion(models.Model):
    poin = models.IntegerField()
    created_by = models.ForeignKey("custom_admin.Account", on_delete=models.CASCADE)
    assesment = models.ForeignKey("Assesment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.soal} - {self.poin}"


class Question(models.Model):
    soal = models.TextField()
    jawaban = models.TextField()
    poin = models.IntegerField()
    assement_question = models.ForeignKey("AssesmentQuestion", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Skors(models.Model):
    skor = models.IntegerField()
    mahasiswa = models.ForeignKey("custom_admin.Account", on_delete=models.CASCADE)
    assesment = models.ForeignKey("Assesment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Question)
def update_assment_question(sender, instance, **kwarg):
    question = sender.objects.filter(assement_question=instance.assement_question)
    instance.assement_question.poin = 0
    for x in question:
        instance.assement_question.poin += x.poin
    instance.assement_question.save()


@receiver(post_delete, sender=Question)
def update_assment_question_delete(sender, instance, **kwarg):
    question = sender.objects.filter(assement_question=instance.assement_question)
    instance.assement_question.poin = 0
    for x in question:
        instance.assement_question.poin -= x.poin
    instance.assement_question.save()
