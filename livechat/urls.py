from django.conf.urls.defaults import patterns, url
from livechat import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.show, name='show'),
)
