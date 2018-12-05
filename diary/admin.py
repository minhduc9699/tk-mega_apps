from django.contrib import admin
from .models import Diary, NoteForEach
# Register your models here.


class DiaryAdmin(admin.ModelAdmin):
  list_display = ["session_num", "session_name", "date", "author_role"]
  search_fields = ["session_num", "session_name", "author_role"]
  list_filter = ["date", "author_role"]


admin.site.register(Diary, DiaryAdmin)
admin.site.register(NoteForEach)
