from forms import *
from feed.models import User_profile
from feed.models import Favorites




def user_created(sender, user, request, **kwargs):
    form = UserRegForm(request.POST)
    data = User_profile(user=user)
    data.sex = form.data["sex"]
    data.birth_date = form.data["birth_date"]
    favorite = Favorites()
    favorite.title = form.data["favorite_topics"]
    favorite.save()
    data.favorite_topics =  favorite
    data.save()

  
from registration.signals import user_registered
user_registered.connect(user_created)    