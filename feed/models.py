from urlparse import urlparse
import feedparser
from dateutil import parser
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

class Feed(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    tags = TaggableManager()
    moderator = models.ForeignKey(User, related_name='moderated_feeds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def domain(self):
        return urlparse(self.url).netloc

    def get_absolute_url(self):
        return reverse('stories:story_detail', args=(self.id,))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        news = feedparser.parse(self.url)
        self.title = news.feed.title
        super(Feed, self).save(*args, **kwargs) 
        

    def initclasses(self):
        news = feedparser.parse(self.url)
        for post in news['entries'] :
            story = Story.create(post.get('title', '') , post.get('link', ''), self, self.moderator, parser.parse(post.get('published', '')), parser.parse(post.get('updated', '')))
            story.save()
            for s_tags in self.tags.all():
                story.tags.add(s_tags)
            story.save()

    
class Story(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    tags = TaggableManager()
    points = models.IntegerField(default=1)
    source = models.ForeignKey(Feed, related_name='feeds_strories')
    moderator = models.ForeignKey(User, related_name='moderated_stories')
    voters = models.ManyToManyField(User, related_name='liked_stories')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    @property
    def domain(self):
        return urlparse(self.url).netloc

    def get_absolute_url(self):
        return reverse('stories:story_detail', args=(self.id,))

    def __unicode__(self):
        return self.title

    @classmethod
    def create(cls, title, url, source, moderator, created_at, updated_at):
    	story = cls(title=title, url=url, source=source, moderator=moderator, created_at = created_at, updated_at=updated_at)    	
    	return story

        
    class Meta:
        verbose_name_plural = "stories"    




class Favorites(models.Model):
    title = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.title



class User_profile(models.Model):
    user=models.ForeignKey(User, unique=True)
    birth_date = models.DateTimeField();
    sex = models.CharField(max_length = 6)
    favorite_topics = models.ForeignKey(Favorites, related_name = 'favorites_profiles')


    def __unicode__(self):
        return self.user.user_name






class Comment(models.Model):
    story = models.ForeignKey(Story, related_name='comments')
    body = models.TextField()

