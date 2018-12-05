from django.urls import path
from . import views

app_name = "diary"

urlpatterns = [path("", views.diary, name="diary"),
               path("api/diaries", views.api_diaries, name=""),
               path("api/dumpdata", views.api_old_diaries_post, name=""),
               path("api/course", views.api_course, name=''),
               path("api/course-detail", views.api_course_detail, name=''),
               path("api/payroll", views.get_payroll, name=''),
               path('api/classroom', views.api_classroom, name='')]
