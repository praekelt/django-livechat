from django.conf.urls.defaults import patterns, url
from livechat.views import LiveChatDetailView

urlpatterns = patterns(
    '',
    url(r'^livechat/(?P<slug>[\w-]+)/$',
        LiveChatDetailView.as_view(),
        name='show_livechat'),
)
