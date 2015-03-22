import autocomplete_light
from feed.models import Favorites



class AutocompleteTaggableItems(autocomplete_light.AutocompleteGenericBase):
    choices = (
        Favorites.objects.all(),
        
    )

    search_fields = (
        
        ('title',),
        
    )


autocomplete_light.register(AutocompleteTaggableItems)