from django.conf.urls import url, include
from . import views
from pll.models import Poll, Vote, Voice, Constituent
from django.views.generic import ListView

app_name = 'pll'
urlpatterns = [
	url(r'^view/$', views.tag, name="tag"),
	url(r'^view/(?P<pk>\d+)/$', views.detail, name="detail"),
	url(r'^vote/(?P<pk>\d+)/$',views.vote, name="vote"),
	url(r'^voice/(?P<pk>\d+)/$',views.voice, name="voice"),
	url(r'^see_voices/$',ListView.as_view(queryset=Voice.objects.all(),template_name="see_voices.html")),
	url(r'^create_poll/$',views.create_poll, name="create_poll"),
	url(r'^register/$',views.ConstituentRegistration,name="ConstituentRegistration"),
	url(r'^login/$',views.LoginRequest,name="LoginRequest"),
	url(r'^logout/$',views.LogoutRequest,name="LogoutRequest"),
	url(r'^profile/(?P<pk>\d+)/$',views.Profile,name="Profile")
]