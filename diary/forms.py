from django import forms
from .models import Diary
from ckeditor.widgets import CKEditorWidget


class AddDiary(forms.Form, forms.ModelForm):
  diary = forms.CharField(widget=CKEditorWidget)
  course_feedback = forms.CharField(widget=CKEditorWidget)
  note_for_each = forms.CharField(widget=CKEditorWidget)

  class Meta:
    model = Diary
    fields = ['author_role']
