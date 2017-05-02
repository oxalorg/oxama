from django.contrib import admin
from django.urls import reverse

from .models import *

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_hyperlink', 'votes', 'created_at')
    exclude = ('slug', )

    def post_hyperlink(self, obj):
        return '<a href="">{}</a>'.format(obj.get_absolute_url())


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'votes', 'created_at')
