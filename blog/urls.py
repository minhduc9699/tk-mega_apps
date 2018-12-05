from django.urls import path
from . import views
from django.conf.urls import url

app_name = "blog"

urlpatterns = [url(r'^$', views.OilListView.as_view(), name="list_oil"),
               url(r'^(?P<pk>\d+)$', views.OilDetailView.as_view(), name="detail_oil"),
               url(r'^api/bonus', views.api_kudo, name='api_bonus'),
               url(r'^bonus', views.bonus, name='bonus'),
               url(r'^like/(?P<pk>\d+)$', views.like, name="like"),
               url(r'^summary', views.ShowOilList.as_view(), name="summary")
               ]
