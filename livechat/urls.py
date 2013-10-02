from django.conf.urls.defaults import patterns, url
from livechat.views import LiveChatDetailView, LiveChatArchiveView

urlpatterns = patterns(
    '',
    url(r'^livechat/(?P<slug>[\w-]+)/$',
        LiveChatDetailView.as_view(),
        name='show_livechat'),
    url(r'^livechat/archive/(?P<slug>[\w-]+)/$',
        LiveChatArchiveView.as_view(),
        name='show_archived_livechat'),
)
