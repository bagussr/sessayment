from django.db import models


class MahasiswaAssesment(models.Model):
    mahasiswa = models.ForeignKey("custom_admin.Account", on_delete=models.CASCADE)
    assesment = models.ForeignKey("dosen.Assesment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
