from django.forms import ModelForm
from .models import Listings

class NewListing(ModelForm):

    class Meta:
        model = Listings
        fields = ["title", "category", "price", "picture"]
        #fileds = '__all__'

