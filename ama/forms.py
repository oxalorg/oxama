from django.forms import ModelForm
from .models import *

class CommentAddForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
