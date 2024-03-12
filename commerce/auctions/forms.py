from django.forms import ModelForm
from .models import Listings, Comment

class NewListing(ModelForm):

    class Meta:
        model = Listings
        fields = ["title", "category", "price", "picture"]
        #fileds = '__all__'


class NewComment(ModelForm):

    class Meta:
        model = Comment
        fields = ["review"]

