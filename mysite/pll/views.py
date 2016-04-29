from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from pll.models import Poll, Vote, Voice, UpDownVote, Constituent
from pll.forms import PollForm, VoteForm, VoiceForm, RegistrationForm, LoginForm
from datetime import datetime
import json, simplejson

TAGS = ['admin','buildings','community','education','events','sustainability','health','parks','safety','sanitation','transportation','other']

# detail view of Poll with Voices

def detail(request,pk):
	if request.method == "POST":
		if request.user.is_authenticated():
			up_or_down = int(request.POST.get('up_or_down'))
			primKey = int(request.POST.get('primKey'))
			if up_or_down == 1:
				if primKey is None:
					return HttpResponse(status=400)
				current_user = request.user
				voice = get_object_or_404(Voice,pk=primKey)
				vote_from_user = len(UpDownVote.objects.filter(voter=current_user,voice=primKey))
				poll = get_object_or_404(Poll,pk=voice.question.id)
				if not vote_from_user:
					upvote = UpDownVote(value=1,voter=current_user,voice=voice)
					upvote.save()
				else:
					upvote = get_object_or_404(UpDownVote,voter=current_user,voice=primKey)
					if (upvote.value != 1):
						upvote.value = 1
					else:
						upvote.value = 0
					upvote.save()
				user_vote = upvote.value
				updown_votes = UpDownVote.objects.filter(voice=voice.id)  
				voice.updown_votes = 0
				for vt in updown_votes:
					voice.updown_votes += vt.value
				net_user_votes = voice.updown_votes
				print(net_user_votes)
				poll_num = poll.id
				print(net_user_votes, poll_num)
				return HttpResponse(json.dumps({"net_user_votes": net_user_votes, "user_vote": user_vote}),content_type='application/json')
			if up_or_down == 2:
				if primKey is None:
					return HttpResponse(status=400)
				current_user = request.user
				voice = get_object_or_404(Voice,pk=primKey)
				vote_from_user = len(UpDownVote.objects.filter(voter=current_user,voice=primKey))
				poll = get_object_or_404(Poll,pk=voice.question.id)
				if not vote_from_user:
					downvote = UpDownVote(value=-1,voter=current_user,voice=voice)
					downvote.save()
				else:
					downvote = get_object_or_404(UpDownVote,voter=current_user,voice=primKey)
					if (downvote.value != -1):
						downvote.value = -1
					else:
						downvote.value = 0
					downvote.save()
				user_vote = downvote.value
				updown_votes = UpDownVote.objects.filter(voice=voice.id)  
				voice.updown_votes = 0
				for vt in updown_votes:
					voice.updown_votes += vt.value
				net_user_votes = voice.updown_votes
				poll_num = poll.id
				print(net_user_votes, poll_num)
				return HttpResponse(json.dumps({"net_user_votes": net_user_votes, "user_vote": user_vote}),content_type='application/json')
		else:
			return HttpResponse(error)
	message = ""
	if request.user.is_authenticated():
		current_user = request.user
		vote_from_user = len(Vote.objects.filter(voter=current_user,question=pk))
		if vote_from_user:
			message = "Voted"

	poll = get_object_or_404(Poll,pk=pk)
	votes = Vote.objects.filter(question=pk)
	voices = Voice.objects.filter(question=pk).order_by('-pub_date')[:10]

	for v in voices:
		if request.user.is_authenticated():
			there_are_updown_votes = len(UpDownVote.objects.filter(voice=v.id,voter=current_user))
			if there_are_updown_votes:
				vtr = get_object_or_404(UpDownVote,voice=v.id,voter=current_user)
				v.uservote = vtr.value 

			updown_votes = UpDownVote.objects.filter(voice=v.id)  
			v.updown_votes = 0
			for vt in updown_votes:
				v.updown_votes += vt.value

	poll.ballots = len(votes)
	ballots = poll.ballots

	total = 0
	for v in votes:
		total += v.ballot

	if poll.ballots > 0:
		poll.avg_vote = total / ballots
		if poll.avg_vote > 1:
			poll.result = "Very Positive"
		elif poll.avg_vote > 0.5:
			poll.result = "Positive"
		elif poll.avg_vote < 0.5 and poll.avg_vote > -0.5:
			poll.result = "Neutral"
		elif poll.avg_vote < -0.5 and poll.avg_vote > -1:
			poll.result = "Negative"
		elif poll.avg_vote < -1:
			poll.result = "Very Negative"
	else:
		poll.result = ""
	return render(request,'detail.html',{'poll': poll, 'voices': voices, 'message': message})

# def up_vote(request,pk):
# 	if request.user.is_authenticated():
# 		current_user = request.user
# 		voice = get_object_or_404(Voice,pk=pk)
# 		vote_from_user = len(UpDownVote.objects.filter(voter=current_user,voice=pk))
# 		poll = get_object_or_404(Poll,pk=voice.question.id)
# 		if not vote_from_user:
# 			upvote = UpDownVote(value=1,voter=current_user,voice=voice)
# 			upvote.save()
# 		else:
# 			upvote = get_object_or_404(UpDownVote,voter=current_user,voice=pk)
# 			if (upvote.value != 1):
# 				upvote.value = 1
# 			else:
# 				upvote.value = 0
# 			upvote.save()
# 		updown_votes = UpDownVote.objects.filter(voice=voice.id)  
# 		voice.updown_votes = 0
# 		for vt in updown_votes:
# 			voice.updown_votes += vt.value
# 		net_user_votes = voice.updown_votes
# 		poll_num = poll.id
# 		return HttpResponse(json.dumps({'net_user_votes': net_user_votes ,'poll_num': poll_num}),content_type='application/json')
# 	else:
# 		return HttpResponseRedirect('/polls/login/')

# def down_vote(request,pk):
# 	if request.user.is_authenticated():
# 		current_user = request.user
# 		voice = get_object_or_404(Voice,pk=pk)
# 		vote_from_user = len(UpDownVote.objects.filter(voter=current_user,voice=pk))
# 		poll = get_object_or_404(Poll,pk=voice.question.id)
# 		if not vote_from_user:
# 			downvote = UpDownVote(value=-1,voter=current_user,voice=voice)
# 			downvote.save()
# 		else:
# 			downvote = get_object_or_404(UpDownVote,voter=current_user,voice=pk)
# 			if (downvote.value != -1):
# 				downvote.value = -1
# 			else:
# 				downvote.value = 0
# 			downvote.save()
# 		updown_votes = UpDownVote.objects.filter(voice=voice.id)  
# 		voice.updown_votes = 0
# 		for vt in updown_votes:
# 			voice.updown_votes += vt.value
# 		net_user_votes = voice.updown_votes
# 		poll_num = poll.id
# 		return HttpResponse(json.dumps({'net_user_votes': net_user_votes ,'poll_num': poll_num}),content_type='application/json')
			
# 	else:
# 		return HttpResponseRedirect('/polls/login/')


# Vote form
def vote(request,pk):
	if request.user.is_authenticated():
		current_user = request.user
		poll = get_object_or_404(Poll,pk=pk)
		vote_from_user = len(Vote.objects.filter(voter=current_user,question=pk))
		page_message = 'Cast your ballot: '
		if vote_from_user:
			page_message = 'Change your ballot: '
		if request.method == 'POST':
			form = VoteForm(request.POST)
			if form.is_valid():
				if not vote_from_user:
					vote = Vote(voter=current_user,question=poll,ballot=form.cleaned_data['ballot'])
				else:
					vote = get_object_or_404(Vote,voter=current_user,question=pk)
					vote.ballot = form.cleaned_data['ballot']
				vote.save()
				return HttpResponseRedirect('/polls/view/%d/' %poll.id)
		else:
			form = VoteForm()
		return render(request,'vote.html',{'poll': poll, 'form': form, 'page_message': page_message})
	else:
		return HttpResponseRedirect('/polls/login/')

# Voice form
def voice(request,pk):
	if request.user.is_authenticated():
		current_user = request.user
		poll = get_object_or_404(Poll,pk=pk)
		if request.method == 'POST':
			form = VoiceForm(request.POST)
			if form.is_valid():
				voice = Voice(author=current_user,pub_date=datetime.now(),question=poll,opinion=form.cleaned_data['opinion'])
				voice.save()
				return HttpResponseRedirect('/polls/view/%d/' %poll.id)

		else:
			form = VoiceForm()

		return render(request,'voice.html',{'poll': poll, 'form': form})
	else:
		return HttpResponseRedirect('/polls/login/')

def create_poll(request):
	if request.user.is_authenticated():
		current_user = request.user
		if request.method == 'POST':
			form = PollForm(request.POST)
			if form.is_valid():
				poll = Poll(author=current_user,pub_date=datetime.now(),question=form.cleaned_data['question'],tag=form.cleaned_data['tag'])
				poll.save()
				return HttpResponseRedirect('/polls/view/')
		else:
			form = PollForm()
		return render(request,'create_poll.html',{'form': form})
	else:
		return HttpResponseRedirect('/polls/login/')

def tag(request):
	if request.method == "POST":
		tagname = str(request.POST.get("tagname",None))
		if tagname == "all":
			return HttepResponse(error)
		polls_with_tag = Poll.objects.filter(tag=tagname).order_by('ballots')
		if len(polls_with_tag) == 0:
			return HttpResponse(error)
		else:
			other_tags = [T for T in TAGS if T != tagname]
			print(other_tags)
			return HttpResponse(json.dumps({"tagname": tagname, "other_tags": other_tags}), content_type='application/json')
	else:
		all_polls = {}
		for T in TAGS:
			polls_of_type = Poll.objects.filter(tag=T).order_by('ballots')
			if len(polls_of_type) > 0:
				all_polls[T] = polls_of_type
		all_polls = all_polls.items()
		return render(request,'list.html',{'all_polls': all_polls})

# register constituents
def ConstituentRegistration(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/polls/view/')
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'],password=form.cleaned_data['password'])
			user.save()
			constituent = Constituent(user=user)
			constituent.save()
			return HttpResponseRedirect('/polls/login/')
		else:
			render_to_response('register.html',{'form': form},context_instance=RequestContext(request))
	else:
		'''user is not submitting a form, show them a blank registration form'''
		form = RegistrationForm()
		context = {'form': form}
		return render_to_response('register.html',context,context_instance=RequestContext(request))

def LoginRequest(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/polls/view/')
	if request.method == 'POST':
		form = LoginForm(request.POST) #request.POST
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			constituent = authenticate(username=username,password=password)
			if constituent is not None:
				login(request,constituent) #just login!
				return HttpResponseRedirect('/polls/view/')
			else:
				return render_to_response('login.html',{'form': form},context_instance=RequestContext(request))
		else:
			return render_to_response('login.html',{'form': form},context_instance=RequestContext(request))
	else:
		'''user is not submitting the form, show the login form'''
		form = LoginForm() #empty paren
		context = {'form': form}
		return render_to_response('login.html',context,context_instance=RequestContext(request)) 

def LogoutRequest(request):
	logout(request)
	return HttpResponseRedirect('/polls/view/')

def Profile(request,pk):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/polls/login')
	this_user = get_object_or_404(User,pk=pk)
	user_polls = Poll.objects.filter(author=pk).order_by('ballots')
	user_voices = Voice.objects.filter(author=pk).order_by('updown_votes')
	user_votes = Vote.objects.filter(voter=pk)

	ballots = 0
	avg_ballots = 0

	updown_votes = 0
	avg_updown_votes = 0

	for p in user_polls:
		ballots += p.ballots
	for v in user_voices:
		updown_votes += v.updown_votes

	num_polls = len(user_polls)
	num_voices = len(user_voices)
	num_votes = len(user_votes)

	if num_polls > 0:
		avg_ballots = ballots / num_polls
	if num_voices > 0:
		avg_updown_votes = updown_votes / num_voices

	user_score = num_polls + num_voices + avg_ballots + avg_updown_votes + num_votes

	context = {'this_user': this_user,'user_score': user_score}

	if num_polls > 0:
		context.update({'user_polls': user_polls})
	if num_voices > 0:
		context.update({'user_voices': user_voices})

	pollster = False
	superPollster = False
	vocalContributor = False
	trustedVoice = False
	activeVoter = False

	polls_threshold = 10
	voices_threshold = 50
	votes_threshold = 50
	avg_ballots_threshold = 50 
	avg_updown_threshold = 5

	if num_polls > polls_threshold:
		if avg_ballots > ballots_threshold:
			superPollster = True
		else:
			pollster = True
	if num_voices > voices_threshold:
		if avg_updown_votes > avg_updown_threshold:
			trustedVoice = True
		else:
			vocalContributor = True

	if num_votes > votes_threshold:
		activeVoter = True

	context.update({'pollster': pollster, 'superPollster': superPollster, 'vocalContributor':vocalContributor,'trustedVoice':trustedVoice, 'activeVoter':activeVoter})

	return render(request,'profile.html',context)