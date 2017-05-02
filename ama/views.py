from datetime import datetime

from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction
from django.db.models import F, Count
from django.utils import timezone
from ratelimit.decorators import ratelimit

from .models import *
from .forms import *
from . import utils


# Create your views here.
def ama_index(request):
    posts = Post.objects.annotate(Count('comment')).filter(expires_at__lt=datetime.now())
    context = {'posts': posts}
    return render(request, 'ama/index.html', context)


def ama_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.starts_at < timezone.now():
        comments = Comment.objects.filter(post=post)
        context = {'post': post, 'nodes': comments}
        return render(request, 'ama/post.html', context)
    else:
        return render(request, 'ama/post_landing.html', {'post': post})


@ratelimit(key='ip', rate='10/m')
@ratelimit(key='ip', rate='40/h')
def like_comment(request):
    if getattr(request, 'limited', False):
        # if the request was limited act as if everything
        # went smoothly ¯\_(ツ)_/¯
        pass
        # return JsonResponse({'status': 'KIK!'})
    elif request.method == 'POST':
        return JsonResponse(status=400)

    try:
        comment_id = request.GET['comment_id']
    except LookupError:
        return JsonResponse(status=404)

    with transaction.atomic():
        with Comment.objects.disable_mptt_updates():
            comment = Comment.objects.get(pk=comment_id)
            comment.votes = F('votes') + 1
            comment.save()
    # TODO: still expensive, but much better
    if Comment.objects.get(pk=comment_id).votes % 4 == 0:
        Comment.objects.rebuild()

    return JsonResponse({'status': 'Success!'})

class CommentCreate(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'ama/comment_add.html'

    def get_success_url(self):
        return reverse(ama_post, args=[self.kwargs['ama_id']])

    def form_valid(self, form):
        post_id = self.kwargs['ama_id']
        # parent == None means that the comment is a reply to the ama
        # instead of being a reply to another comment
        parent = None
        parent_id = self.kwargs.get('cmt_id', None)
        if parent_id is not None:
            parent = get_object_or_404(Comment, pk=parent_id)

        if self.request.user.is_authenticated:
            name = self.request.user.username
            author = self.request.user
        else:
            name = utils.get_random_name()
            author = None
        content = form.cleaned_data['content']

        self.object = Comment(name=name, content=content, post_id=post_id, author=author)
        self.object.insert_at(parent, save=True)
        return HttpResponseRedirect(self.get_success_url())

