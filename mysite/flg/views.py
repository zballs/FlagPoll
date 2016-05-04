from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from pll.models import Poll, Vote, Voice
from flg.models import Flag

from flg.agg_clust import AgglomerativeClustering
# Import other sentiment analysis modules...

# Create your views here.
def flag(request):
	flags = Flag.objects.all()

	for f in flags:
		count = 0
		polls = Poll.objects.filter(tag=f.tag)
		for p in polls:
			votes = Vote.objects.filter(question=p.id)
			for v in votes:
				f.avg_vote += v.ballot
				count += 1

		if count > 0:
			f.avg_vote = f.avg_vote / count
		if f.avg_vote > 1:
			f.result = "Very Positive"
		elif f.avg_vote > 0.5:
			f.result = "Positive"
		elif f.avg_vote < -1:
			f.result = "Very Negative"
		elif f.avg_vote < -0.5:
			f.result = "Negative"
		elif count == 0:
			f.result = ""
		elif len(polls) == 0:
			f.result = ""
		else:
			f.result = ""


	return render(request,'flag.html',{'flags': flags})

def flag_detail(request,pk):
	flag = get_object_or_404(Flag, pk=pk)
	related_polls = Poll.objects.filter(tag=flag.tag)
	voice_list = []
	for p in related_polls:
		voices = Voice.objects.filter(question=p.id)
		for v in voices:
			voice_list.append(v)

	return render(request,'flag_detail.html',{'voice_list': voice_list,'related_polls': related_polls,'flag': flag})