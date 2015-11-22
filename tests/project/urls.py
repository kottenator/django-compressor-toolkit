from django.conf.urls import url
from django.views.generic.base import TemplateView


urlpatterns = [
    url('^$', TemplateView.as_view(template_name='home/index.html')),
]
