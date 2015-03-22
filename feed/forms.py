from django.forms import ModelForm
from registration.forms import RegistrationForm
from feed.models import User_profile
from feed.models import Story
from feed.models import Feed
from feed.models import Favorites
from django import forms
from taggit.forms import TagField
import django.forms.extras.widgets 


class StoryForm(ModelForm):
    class Meta:
        model = Story
        exclude = ('points', 'moderator', 'voters','created_at','updated_at','source')


class UserRegForm(RegistrationForm):
	SEX = (('male','Male'),('female','Female'))
	birth_date = forms.DateField()
	sex = forms.ChoiceField(widget = forms.RadioSelect(), choices = SEX)
	topics=Favorites.objects.all() 
	#favorite_topics = forms.ChoiceField(queryset=topics,widget=forms.Select(attrs={'class':'title', })) 
	favorite_topics = forms.ModelChoiceField(queryset=topics,widget=forms.Select(attrs={'class':'title', })) 


class FeedForm(ModelForm):
	class Meta:
		model = Feed
		exclude = ('title', 'moderator', 'created_at', 'updated_at')

	