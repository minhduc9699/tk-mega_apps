from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Oil, LikeOil, UserProfile
import json
import datetime


# Create your views here.


@method_decorator(login_required, name='dispatch')
class OilListView(ListView):
  context_object_name = "oils"
  model = Oil
  paginate_by = 6

  def get_queryset(self):
    qs = super(OilListView, self).get_queryset()
    search_tearm = self.request.GET.get('s', None)
    qs = self.model.objects.filter(on_payroll=True).order_by("-date")
    if search_tearm is not None:
      qs = qs.filter(Q(title__icontains=search_tearm) |
                     Q(question__icontains=search_tearm) |
                     Q(anwser__icontains=search_tearm)
                     )
    # if len(qs) == 0:
    #   qs = 
    return qs

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['like'] = [LikeOil.objects.filter(oil_like=oil).count() for oil in context["oils"]]
      context['user'] = UserProfile.objects.get(user=self.request.user)
      return context


class OilDetailView(DetailView):
  context_object_name = "oil_detail"
  model = Oil
  template_name = "blog/oil_detail.html"

  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs)
  #   context["like"] = len(LikeOil.objects.filter(oil_like=self.kwargs["pk"]))
  #   return context


@csrf_exempt
def like(request, pk):
  user = UserProfile.objects.get(user=request.user)
  post = Oil.objects.get(id=pk)
  total_like = len(LikeOil.objects.filter(oil_like=post))
  if request.method == "GET":
    try:
      like = LikeOil.objects.get(user=user, oil_like=post)
      data = {"liked": 1,
              "post_id": post.pk,
              "user_id": user.pk,
              "total_like": total_like}
      return JsonResponse({"data": data})
    except BaseException:
      data = {"liked": 0,
              "total_like": total_like}
      return JsonResponse({"data": data})
  elif request.method == "POST":
    like, create = LikeOil.objects.get_or_create(user=user, oil_like=post)
    if not create:
      like.delete()
    return JsonResponse({"data": {"total_lile": total_like}})
  else:
    return JsonResponse({"data": "None"})


def api_kudo(request):
  # get time from FE
  start_time = request.GET['start_time']
  stop_time = request.GET['stop_time']
  start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
  stop_time = datetime.datetime.strptime(stop_time, "%Y-%m-%d")
  # querry in data base
  oils = Oil.objects.filter(date__range=[start_time, stop_time], on_payroll=True)
  if not oils:
    return JsonResponse({"success": 0, "message": "not found any record"})
  # cal user kudo
  temp_sum_kudo = 0
  list_contrib = []
  list_user_kudo = []
  all_contributor = UserProfile.objects.all()

  for contrib in all_contributor:
    for oil in oils:
      if oil.contributor == contrib:
        list_contrib.append(oil)
    for oil_by_user in list_contrib:
      temp_sum_kudo += oil_by_user.kudo

    money = temp_sum_kudo * 5000
    user_kudo = {"user_id": contrib.pk,
                 "username": contrib.user.username,
                 "first_name": contrib.user.first_name,
                 "last_name": contrib.user.last_name,
                 "kudo": temp_sum_kudo,
                 "money": money
                 }
    list_user_kudo.append(user_kudo)
    temp_sum_kudo = 0
    list_contrib = []

  return JsonResponse({"data": list_user_kudo})


def bonus(request):
  return render(request, "blog/Bonus.html")


class ShowOilList(ListView):
  context_object_name = "oils"
  model = Oil
  template_name = "blog/show_oil.html"

  def get_queryset(self):
    start_date = self.request.GET.get("start_date", None)
    stop_date = self.request.GET.get("stop_date", None)
    user = UserProfile.objects.get(user=self.request.user)
    qs = super(ShowOilList, self).get_queryset()
    if start_date and stop_date is not None:
      qs = self.model.objects.filter(on_payroll=True, date__range=[start_date, stop_date]).order_by("-date")
    else:
      qs = self.model.objects.filter(on_payroll=True).order_by("-date")
    qs = qs.filter(Q(contributor=user))
    return qs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = UserProfile.objects.get(user=self.request.user)
    oils = Oil.objects.filter(on_payroll=True, contributor=user)
    list_kudo = [oil.kudo for oil in oils]
    context["user"] = user
    context['like'] = [LikeOil.objects.filter(oil_like=oil).count() for oil in context["oils"]]
    context["total_kudo"] = sum(list_kudo)
    return context
