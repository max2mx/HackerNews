import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required

from feed.models import Feed
from feed.models import Story
from feed.forms import StoryForm
from feed.forms import FeedForm

def score(story, gravity=1.8, timebase=120):
    points = (story.points - 1)**0.8
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    age = int((now - story.created_at).total_seconds())/60

    return points/(age+timebase)**1.8

def top_stories(top=180, consider=1000):
    latest_stories = Story.objects.all().order_by('-created_at')[:consider]
    ranked_stories = sorted([(score(story), story) for story in latest_stories], reverse=True)
    return [story for _, story in ranked_stories][:top]

@login_required
def feeds(request):
    user = request.user
    related_feeds = user.moderated_stories.all().order_by('-created_at')
    stories = top_stories(top = 30)
    liked_stories = user.liked_stories.filter(id__in=[story.id for story in stories])
    return render(request, 'feeds/feeds.html', {
        'feeds' : related_feeds,
        'user' : user,
        'liked_stories' : liked_stories
        })


def index(request):
    stories = top_stories(top=30)
    if request.user.is_authenticated():
        liked_stories = request.user.liked_stories.filter(id__in=[story.id for story in stories])
    else:
        liked_stories = []
    return render(request, 'stories/index.html', {
        'stories': stories,
        'user': request.user,
        'liked_stories': liked_stories
    })

@login_required
def story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.moderator = request.user
            story.save()
            return HttpResponseRedirect('/')
    else:
        form = StoryForm()
    return render(request, 'stories/story.html', {'form': form})

@login_required
def feed(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            s_tags = form.cleaned_data['tags']
            feed = form.save(commit=False)
            feed.moderator = request.user
            # for tag in s_tags:
            #     feed.tags.add(tag)            
            feed.save()
            form.save_m2m()
            feed.initclasses()
            return HttpResponseRedirect('/')
    else:
        form = FeedForm()        
    return render(request, 'feeds/feed.html', {'form': form})    


def story_detail(request, story_id):
    return HttpResponse("Story Detail View")

@login_required
def vote(request):
    story = get_object_or_404(Story, pk=request.POST.get('story'))
    story.points += 1
    story.save()
    user = request.user
    user.liked_stories.add(story)
    user.save()
    return HttpResponse()

