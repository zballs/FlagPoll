from django.contrib import admin
from django.forms import ModelForm 
from pll.models import Poll, Vote, Voice, UpDownVote

class PollAdmin(admin.ModelAdmin):
	exclude = ("ballots","avg_vote","result")

class VoteAdmin(admin.ModelAdmin):
	exclude = ("voter","question")

class VoiceAdmin(admin.ModelAdmin):
	exclude = ("author","pub_date","question","updown_votes","uservote")

class UpDownVoteAdmin(admin.ModelAdmin):
	exclude = ("value","voter")

admin.site.register(Poll,PollAdmin)