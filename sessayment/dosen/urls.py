from django.urls import path

from . import views

urlpatterns = [
    path("schedule", views.schedule, name="dosen"),
    path("schedule/<int:id>", views.schedule_action, name="schedule.action"),
    path("schedule/edit/<int:id>", views.ScheduleEditView.as_view(), name="schedule.edit"),
    path("schedule/delete/<int:id>", views.ScheduleEditView.delete, name="schedule.delete"),
    path("schedule/add", views.ScheduleAddView.as_view(), name="schedule.add"),
    path("schedule/<int:id>/assesment", views.assesment, name="schedule.assesment"),
    path("schedule/<int:id>/question", views.QuestionAddView.as_view(), name="schedule.add.question"),
    path("schedule/<int:id>/question/edit", views.QuestionAddView.edit, name="schedule.edit.question"),
    path("schedule/<int:id>/question/<int:question_id>", views.QuestionAddView.detail, name="schedule.detail.question"),
    path("schedule/<int:id>/question/<int:question_id>", views.QuestionAddView.delete, name="schedule.delete.question"),
    path("schedule/<int:id>/score", views.score, name="score"),
]
