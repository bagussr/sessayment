# Generated by Django 4.2.3 on 2023-08-08 02:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("custom_admin", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Assesment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "jenis_ujian",
                    models.BigIntegerField(
                        choices=[(1, "UTS"), (2, "UAS"), (3, "Kuis")]
                    ),
                ),
                ("tanggal", models.DateField()),
                ("waktu_mulai", models.TimeField()),
                ("waktu_selesai", models.TimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "mata_kuliah",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="custom_admin.matakuliah",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AssesmentQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("poin", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "assesment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dosen.assesment",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Skors",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("skor", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "assesment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dosen.assesment",
                    ),
                ),
                (
                    "mahasiswa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("soal", models.TextField()),
                ("jawaban", models.TextField()),
                ("poin", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "assement_question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dosen.assesmentquestion",
                    ),
                ),
            ],
        ),
    ]
