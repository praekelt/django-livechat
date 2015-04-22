from django.conf.urls.defaults import patterns, url
from livechat.views import LiveChatDetailView, LiveChatArchiveView

urlpatterns = patterns(
    '',
    url(r'^livechat/archive/$',
        LiveChatArchiveView.as_view(),
        name='show_archived_livechat'),
    url(r'^livechat/(?P<slug>[\w-]+)/$',
        LiveChatDetailView.as_view(),
        name='show_livechat'),

)
