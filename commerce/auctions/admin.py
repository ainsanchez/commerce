from django.contrib import admin

from .models import User, Listings, Watchlist, Bid, Comment

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "review")

admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comment, CommentAdmin)
