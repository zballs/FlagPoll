from django.contrib import admin
from django.forms import ModelForm 
from flg.models import Flag

class FlagAdmin(admin.ModelAdmin):
	exclude = ("avg_vote","result","sentiment")

admin.site.register(Flag,FlagAdmin)