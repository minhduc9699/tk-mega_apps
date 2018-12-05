from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from services import lms, payroll
import json
from addict import Dict
from .models import Diary, NoteForEach
from .forms import AddDiary
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db import transaction
from datetime import datetime
from mega_apps.base import get_env_variable
from django.shortcuts import get_object_or_404
import requests

PAYROLL_PASSWORD = get_env_variable("PAYROLL_PASSWORD")


def get_token(request):
  try:
    TOKEN = request.session["access_token"]
    headers = {"access_token": TOKEN}
    return headers
  except KeyError:
    logout(request)
    return HttpResponseRedirect("/login/logout")


@login_required
def diary(request):
  headers = get_token(request)
  user_data = lms.auth.get(headers=headers)
  if "data" not in user_data.json():
    logout(request)
    return HttpResponseRedirect("/login")
  else:
    form = AddDiary()
    return render(request, 'diary/diary.html', {'form': form})


def get_classroom(request):
  lms.classroom.url += "?listAll=1"
  headers = get_token(request)
  r = lms.classroom.get(headers=headers)
  data = r.json()
  if "data" not in data:
    return None
  classroom_data = data['data']['class']
  for classroom in classroom_data:
    del classroom['playlists']
    classroom_id = classroom["_id"]
    diaries = Diary.objects.filter(classroom_id=classroom_id).order_by('session_num')
    for member in classroom["members"]:
      notes = NoteForEach.objects.filter(classroom__classroom_id=classroom_id,
                                         member_id=member["_id"])
      n_dict = [{"_id": n.id,
                 "diary_id": n.classroom.id,
                 "note": n.note,
                 "session_num": n.classroom.session_num} for n in notes]
      notes_dict = {n.member_id: n_dict for n in notes}
      notes = notes_dict.get(member["_id"], 0)
      member["notes"] = notes
    d_dict = [{f"session {d.session_num}": {"_id": d.id,
                                            "author_id": d.author_id,
                                            "author_role": d.author_role,
                                            "date": d.date,
                                            "session_num": d.session_num,
                                            "session_name": d.session_name,
                                            "diary": d.diary,
                                            "feedback": d.course_feedback
                                            }} for d in diaries]
    diary_merged = {}
    for d in d_dict:
      for key, val in d.items():
        if key not in diary_merged:
          diary_merged[key] = []
        diary_merged[key].append(val)

    classroom["sessions"] = [{"session_num": k, "diaries": v} for k, v in diary_merged.items()]

  lms.classroom.url = lms.reset_url_classroom
  return classroom_data


@csrf_exempt
def api_classroom(request):
  if request.method == "GET":
    classroom_data = get_classroom(request)
    return JsonResponse({"user_role": request.session["role"],
                         "data": classroom_data})


def api_course(request):
  lms.courses.url += "?listALl=1"
  headers = get_token(request)
  course_response = lms.courses.get(headers=headers).json()
  course_data = course_response["data"]
  classroom_data = get_classroom(request)
  class_in_course = []
  for course in course_data:
    for classroom in classroom_data:
      if classroom["course"] == course["course"]:
        class_in_course.append(classroom)
    course["classrooms"] = class_in_course
    class_in_course = []
  lms.courses.url = lms.reset_url_course
  return JsonResponse({"user_id": request.session["user_id"],
                       "user_role": request.session["role"],
                       "data": course_data})


def api_course_detail(request):
  headers = get_token(request)
  course_id = request.GET["course_id"]
  if "course_id" not in request.GET:
    return JsonResponse({'success': 0,
                         'message': '\'course_id\' not specified',
                         })
  course_response = lms.courses.get(course_id, headers=headers).json()
  course_data = course_response["data"]
  classroom_data = get_classroom(request)
  class_in_course = []
  for classroom in classroom_data:
    if classroom["course"] == course_data["course"]:
      class_in_course.append(classroom)

  course_data["classrooms"] = class_in_course
  return JsonResponse({"data": course_data})


@csrf_exempt
def api_diaries(request):
  if "classroom_id" not in request.GET:
    return JsonResponse({'success': 0,
                         'message': '\'classroom_id\' not specified',
                         })
  classroom_id = request.GET["classroom_id"]
  if request.method == "GET":
    return api_diaries_get(request, classroom_id)
  elif request.method == "POST":
    return api_diaries_post(request, classroom_id)
  elif request.method == "PUT":
    return api_diaries_update(request, classroom_id)
  elif request.method == "DELETE":
    return api_diaries_delete(request, classroom_id)


def api_diaries_get(request, classroom_id):
  headers = get_token(request)
  classroom_response = lms.classroom.get(classroom_id, headers=headers).json()

  if "data" not in classroom_response:
    return JsonResponse({"success": 0, "message": 'Could not find classroom', })

  classroom_data = Dict(classroom_response["data"])
  diaries = Diary.objects.filter(classroom_id=classroom_id)
  for member in classroom_data.members:
    notes = NoteForEach.objects.filter(classroom__classroom_id=classroom_id, member_id=member._id)
    n_dict = [{"note": n.note,
               "session_num": n.classroom.session_num} for n in notes]
    notes_dict = {n.member_id: n_dict for n in notes}
    notes = notes_dict.get(member._id, 0)
    member.notes = notes
  del classroom_data.playlists
  classroom_data.diaries = [{'_id': d.id,
                             'author_id': d.author_id,
                             'author_role': d.author_role,
                             'date': d.date,
                             'session_num': d.session_num,
                             'session_name': d.session_name,
                             'diary': d.diary,
                             'feedback': d.course_feedback
                             } for d in diaries]

  return JsonResponse({"data": classroom_data})


def find_course(list_data, key, id):
  for data in list_data:
    if key in data:
      if data[key] == id:
        return data


def get_course_name(long_name):
  if long_name == "Code Intensive":
    course_name = "Code Intensive"
  elif long_name == "Web FullStack":
    course_name = "Fullstack Web"
  elif long_name == "Code For Teen":
    course_name = "C4T (v2)"
  elif long_name == "Code For Everyone":
    course_name = "C4E Big"
  elif long_name == "ReactNative":
    course_name = "React Native"
  return course_name


def get_payroll():
  payroll.payroll.url += f"?masterpassword={PAYROLL_PASSWORD}"
  payroll_res = payroll.payroll.get().json()
  payroll.payroll.url = payroll.reset_url
  return payroll_res


def post_payroll(request, data_response, classroom_id):
  payroll.payroll_post.url += f"?masterpassword={PAYROLL_PASSWORD}"
  payroll_res = get_payroll()
  course_name = get_course_name(data_response["long_name"])
  record_date = datetime.strptime(data_response["date"], '%Y-%m-%d').isoformat()
  course = find_course(payroll_res["courses"], "name", course_name)
  class_no = data_response["class_no"]
  class_name = course_name + " " + str(class_no)
  payroll_post = {"className": class_name,
                  "classNo": class_no,
                  "recordDate": record_date,
                  "code": request.session["code"],
                  "role": data_response["author_role"],
                  "course": course["_id"],
                  "masterPassword": PAYROLL_PASSWORD
                  }
  post = payroll.payroll_post.post(payroll_post).json()
  payroll.payroll_post.url = payroll.reset_post_url
  return post


def del_payrol(id):
  requests.delete(f"http://techkids.vn:7791/api/instructor/record/{id}?masterpassword={PAYROLL_PASSWORD}")


@transaction.atomic
def api_diaries_post(request, classroom_id):
  data_response = json.loads(request.body)
  new_diary, create = Diary.objects.get_or_create(classroom_id=classroom_id,
                                                  author_id=request.session["user_id"],
                                                  author_role=data_response["author_role"],
                                                  date=data_response["date"],
                                                  session_num=data_response["session_num"],
                                                  session_name=data_response["session_name"],
                                                  course_feedback=data_response["feedback"],
                                                  diary=data_response["diary"])
  if create:
    try:
      post_data = post_payroll(request, data_response, classroom_id)
      new_diary.payroll_id = post_data["results"]["_id"]
    except BaseException:
      pass
    new_diary.save()
  for member in data_response["members"]:
    new_note, create = NoteForEach.objects.get_or_create(classroom=new_diary,
                                                         member_id=member["member_id"],
                                                         note=member["note"])
    new_note.save()
  return JsonResponse({"data": data_response})


@transaction.atomic
def api_diaries_update(request, classroom_id):
  data_response = json.loads(request.body)

  diary = Diary.objects.get(id=data_response["_id"])

  diary.classroom_id = classroom_id
  diary.author_id = data_response["author_id"]
  diary.author_role = data_response["author_role"]
  diary.date = data_response["date"]
  diary.session_num = data_response["session_num"]
  diary.session_name = data_response["session_name"]
  diary.course_feedback = data_response["feedback"]
  diary.diary = data_response["diary"]

  diary.save()
  for member in data_response["members"]:
    # memb = json.loads(json.dumps(member))
    note = NoteForEach.objects.get(pk=member["_id"])
    note.member_id = member["member_id"]
    note.note = member["note"]
    note.save()

  return JsonResponse(data_response)


def api_diaries_delete(request, classroom_id):
  data_response = json.loads(request.body)
  data_to_del = get_object_or_404(Diary, pk=data_response["_id"])
  data_to_del.delete()
  try:
    del_payrol(data_to_del.payroll_id)
  except BaseException:
    pass
  return JsonResponse(data_response)



# dump data từ 1 đống cứt
@csrf_exempt
def api_old_diaries_post(request):
  if request.method == "POST":
    data_response = json.loads(request.body)
    n = 1
    name = "old data"
    for d in data_response[0]:
      new_diary = Diary.objects.create(classroom_id=d["id"],
                                       author_id=d["author_id"],
                                       diary=d["note_summary"],
                                       session_name=name,
                                       session_num=n
                                       )
      new_diary.save()
      n += 1
    for d in data_response[1]:
      class_diary = Diary.objects.get(classroom_id=d["diary_id"])
      new_note = NoteForEach.objects.create(classroom=class_diary,
                                            member_id=d["member_id"],
                                            note=d["note"]
                                            )
      new_note.save()
    return JsonResponse({"data": data_response})
  else:
    return JsonResponse({"data": "hello"})
