from django.conf.urls import url
from django.views.generic.base import TemplateView


urlpatterns = [
    url(
        '^scss-file/$',
        TemplateView.as_view(template_name='app/template-with-scss-file.html'),
        name='scss-file'
    ),
    url(
        '^scss-inline/$',
        TemplateView.as_view(template_name='app/template-with-scss-inline.html'),
        name='scss-inline'
    ),
    url(
        '^es6-file/$',
        TemplateView.as_view(template_name='app/template-with-es6-file.html'),
        name='es6-file'
    ),
    url(
        '^es6-inline/$',
        TemplateView.as_view(template_name='app/template-with-es6-inline.html'),
        name='es6-inline'
    )
]
