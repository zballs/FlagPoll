from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from datetime import datetime

CHOICES = ((2,'Very Positive'),(1,'Positive'),(0,'Neutral'),(-1,'Negative'),(-2,'Very Negative'))

TAGS = (('admin','Administration & Finance'),('buildings','Buildings'),('community','Community Development'),('education','Education'),
('events','Events'),('sustainability','Environment and Sustainability'),('health','Health & Human Services'),
('parks','Parks & Rec'),('safety','Public Safety'),('sanitation','Sanitation'),('transportation','Transportation'),('other','Other'))

class Poll(models.Model):
	author = models.ForeignKey(User,default=0)
	pub_date = models.DateTimeField(default=datetime.now())
	tag = models.CharField(max_length=30,choices=TAGS,default="no tag")
	question = models.TextField(max_length=150)
	ballots = models.IntegerField(default=0)
	avg_vote = models.DecimalField(decimal_places=2,max_digits=10,default=0)
	result = models.CharField(max_length=20,default="")

	def __str__ (self):
		return self.question

class Vote(models.Model):
	voter = models.ForeignKey(User,default=0)
	question = models.ForeignKey(Poll)
	ballot = models.IntegerField(choices=CHOICES)
	def __int__ (self):
		return self.ballot

class Voice(models.Model):
	author = models.ForeignKey(User,default=0)
	pub_date = models.DateTimeField(default=datetime.now())
	question = models.ForeignKey(Poll)
	opinion = models.TextField()
	updown_votes = models.IntegerField(default=0)
	uservote = models.IntegerField(default=0)
	def __str__(self):
		return self.opinion

class UpDownVote(models.Model):
	value = models.IntegerField(default=0)
	voter = models.ForeignKey(User,default=0)
	voice = models.ForeignKey(Voice,default=0)
	def __int__(self):
		return self.voter

class Constituent(models.Model):
	user = models.OneToOneField(User)
	def __int__(self):
		return self.user