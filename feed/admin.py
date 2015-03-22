from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from feed.models import Feed
from feed.models import Story
from feed.models import Favorites
from feed.models import User_profile
from django.contrib.auth.models import User

admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
    model = User_profile

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline,]
admin.site.register(User, UserProfileAdmin)


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
admin.site.register(Favorites, FavoritesAdmin)


class FeedAdmin(admin.ModelAdmin):
	list_display = ('title', 'domain', 'moderator', 'created_at', 'updated_at')
	list_filter = ('created_at', 'updated_at')
	search_fields = ('title', 'moderator__username', 'moderator__first_name', 'moderator__last_name')

	fieldsets = [
        ('Story', {
            'fields': ('title', 'url')
        }),
        ('Moderator', {
            'classes': ('collapse',),
            'fields': ('moderator',)
        }),
        ('Change History', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        })
    ]
 	readonly_fields = ('created_at', 'updated_at')
admin.site.register(Feed, FeedAdmin)

class StoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'domain', 'url', 'moderator', 'points', 'created_at', 'updated_at')
	list_filter = ('created_at', 'updated_at')
	search_fields = ('title', 'moderator__username', 'moderator__first_name', 'moderator__last_name')

	fieldsets = [
        ('Story', {
            'fields': ('title', 'url', 'points')
        }),
        ('Moderator', {
            'classes': ('collapse',),
            'fields': ('moderator',)
        }),
        ('Change History', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        })
    ]
   	readonly_fields = ('created_at', 'updated_at')
admin.site.register(Story, StoryAdmin)



