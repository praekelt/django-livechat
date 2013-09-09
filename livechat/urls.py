from django.conf.urls.defaults import patterns, url
from livechat import views

urlpatterns = patterns(
    '',
    url(r'^/livechat/(?P<slug>[\w-]+)/$',
        views.show_livechat,
        name='show_livechat'),
)
