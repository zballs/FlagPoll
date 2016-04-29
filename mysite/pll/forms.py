from django import forms
from django.forms import ModelForm
from pll.models import Poll, Vote, Voice, Constituent
from django.contrib.auth.models import User

class PollForm(ModelForm):
	class Meta:
		model = Poll
		exclude = ("author","pub_date","ballots","avg_vote","result")

class VoteForm(ModelForm):
	class Meta:
		model = Vote
		exclude = ("voter","question",)

class VoiceForm(ModelForm):
	class Meta:
		model = Voice
		exclude = ("author","pub_date","question","updown_votes","uservote")

class RegistrationForm(ModelForm):
	username = forms.CharField(label=(u'Username'))
	email = forms.EmailField(label=(u'Email Address'))
	password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False))
	passwordVerification = forms.CharField(label=(u'Verify Password'),widget=forms.PasswordInput(render_value=False))
	class Meta:
		model = Constituent
		exclude = ("user",)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("That username is already taken, please select another.")

	def clean(self):
		if self.cleaned_data['password'] != self.cleaned_data['passwordVerification']:
			raise forms.ValidationError("The passwords did not match, please try again.")
		return self.cleaned_data

class LoginForm(forms.Form):
	username = forms.CharField(label=(u'Username'))
	password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False))
