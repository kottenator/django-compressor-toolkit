from django.conf.urls import url
from django.views.generic.base import TemplateView


urlpatterns = [
    url(
        '^scss-file/$',
        TemplateView.as_view(template_name='app/template-with-scss-file.html'),
        name='scss-file'
    ),
    url(
        '^inline-scss/$',
        TemplateView.as_view(template_name='app/template-with-inline-scss.html'),
        name='inline-scss'
    ),
]
