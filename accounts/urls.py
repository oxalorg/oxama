from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    url(r'^register/', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url=reverse_lazy('login')
    ), name='register'),
    url(r'', include('django.contrib.auth.urls')),
]
