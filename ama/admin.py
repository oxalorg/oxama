from django.contrib import admin
from django.urls import reverse

from .models import *

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_hyperlink', 'votes', 'starts_at', 'expires_at')
    exclude = ('slug', )

    def post_hyperlink(self, obj):
        return '<a href="{0}">{0}</a>'.format(obj.get_absolute_url())
    post_hyperlink.allow_tags = True
    post_hyperlink.short_description = 'URL/Link to Post'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'votes', 'created_at')
