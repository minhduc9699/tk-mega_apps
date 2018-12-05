from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
# Create your models here.


ROLE_CHOICES = (("instructor", "Instructor"),
                ("mentor", "Mentor"),
                ("coach", "Coach"),
                )


class Diary(models.Model):
  classroom_id = models.CharField(max_length=255)
  author_id = models.CharField(max_length=255)
  author_role = models.CharField(max_length=255, choices=ROLE_CHOICES, default="mentor")
  session_num = models.PositiveIntegerField()
  session_name = models.CharField(max_length=255)
  date = models.DateField(default=datetime.now)
  course_feedback = RichTextField(default=".")
  diary = RichTextField()
  payroll_id = models.CharField(max_length=255, default=".")

  class Meta:
    verbose_name = "Diary"
    verbose_name_plural = "Diaries"

  def __str__(self):
    return "Session " + str(self.session_num) + " " + self.session_name


class NoteForEach(models.Model):
  classroom = models.ForeignKey(Diary, on_delete=models.CASCADE)
  member_id = models.CharField(max_length=2525)
  note = RichTextField()

  def __str__(self):
    return str(self.classroom)
