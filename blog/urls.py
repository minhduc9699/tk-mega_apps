from django.urls import path
from . import views
from django.conf.urls import url

app_name = "blog"

urlpatterns = [path('', views.OilListView.as_view(), name="list_oil"),
               path('<int:pk>', views.OilDetailView.as_view(), name="detail_oil"),
               path('api/bonus', views.api_kudo, name='api_bonus'),
               path('bonus', views.bonus, name='bonus'),
               path('like/<int:pk>', views.like, name="like"),
               path('summary', views.ShowOilList.as_view(), name="summary")
               ]
