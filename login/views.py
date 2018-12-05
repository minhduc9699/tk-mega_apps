from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .forms import LoginForm
from django.contrib import messages
from tk_rest import TKRest
from django.contrib.auth.models import Permission


def index(request):
  next = request.GET.get('next', None)
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data["username"]
      password = form.cleaned_data["password"]
      remember_me = form.cleaned_data["remember_me"]
      data = {"username": username,
              "password": password}
      r = TKRest('https://learn.techkids.vn/api')
      r = r.auth.post(data)

      if r.json()['success'] == 1:
        user_role = r.json()['data']['user']['role']
        request.session["access_token"] = r.json()['data']['access_token']
        request.session["user_id"] = r.json()["data"]["user"]["id"]
        request.session["code"] = r.json()["data"]["user"]["checkCode"]
        save_user_role(request, user_role)
        user, create = User.objects.get_or_create(username=username,
                                                  password=password,
                                                  first_name=r.json()['data']['user']['firstName'],
                                                  last_name=r.json()['data']['user']['lastName'],
                                                  is_staff=True)
        if create:
          set_permission(user, user_role)

        if not remember_me:
          request.session.set_expiry(0)
        else:
          request.session.set_expiry(500000)
        login(request, user)
        if next is None:
          return HttpResponseRedirect(request.path)
        else:
          return HttpResponseRedirect(next)
      else:
        messages.warning(request, 'Username or password incorrect!')
        return render(request, 'diary/diary-login.html', {"form": form, 'next': next})
  else:
    if request.user.is_authenticated:
      return HttpResponseRedirect("/worm")
    else:
      form = LoginForm()
      return render(request, 'diary/diary-login.html', {"form": form, 'next': next})


def set_permission(user, role):
  mentor_permission = ['Can add Diary',
                       'Can change Diary',
                       'Can delete Diary',
                       'Can add note for each',
                       'Can change note for each',
                       'Can delete note for each']
  if role == 1:
    for permiss in mentor_permission:
      permission = Permission.objects.get(name=permiss)
      user.user_permissions.add(permission)


def save_user_role(request, user_role):
  if user_role == 2:
    request.session['role'] = "teacher"
  elif user_role == 3:
    request.session['role'] = "manager"
  else:
    request.session['role'] = "student"


def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/login')
