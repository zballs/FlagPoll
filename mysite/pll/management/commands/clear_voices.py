from django.core.management.base import BaseCommand, CommandError
from pll.models import Voice

class Command(BaseCommand):
	help = 'Write comments to text file for language process and sentiment analysis'

	def handle(self,*args,**options):
		text = ''
		f = open('pll/voices.txt','w')
		f.write(text)
		f.close()
