from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

import markdown2


markdowner = markdown2.Markdown()

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    votes = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def html(self):
        return markdowner.convert(self.content)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    name = models.CharField(max_length=50)
    content = models.TextField(max_length=9001)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    post = models.ForeignKey(Post)
    votes = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['votes']

    def __str__(self):
        return "Comment " + str(self.id)
