from django.conf.urls import url, include
from . import views
from flg.models import Flag

app_name = 'flg'

urlpatterns = [
	url(r'^$',views.flag,name="flag"),
	url(r'^(?P<pk>\d+)/$', views.flag_detail, name="flag_detail")
]