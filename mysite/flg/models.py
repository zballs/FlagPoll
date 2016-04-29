from django.db import models

TAGS = (('admin','Administration & Finance'),('buildings','Buildings'),('community','Community Development'),('education','Education'),
('events','Events'),('sustainability','Environment and Sustainability'),('health','Health & Human Services'),
('parks','Parks & Rec'),('safety','Public Safety'),('sanitation','Sanitation'),('transportation','Transportation'),('other','Other'))

# Create your models here.
class Flag(models.Model):
	tag = models.CharField(max_length=30,choices=TAGS,default="no tag")
	avg_vote = models.DecimalField(decimal_places=2,max_digits=10,default=0)
	result = models.CharField(max_length=30,default="")
	sentiment = models.CharField(max_length=30,default="")

class ConstituentEval(models.Model):
	value = models.DecimalField(decimal_places=2,max_digits=10,default=0)
	