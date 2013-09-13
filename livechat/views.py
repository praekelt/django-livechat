from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django.views.generic.detail import DetailView


from livechat.models import LiveChat

current_site = Site.objects.get_current()


class LiveChatDetailView(DetailView):

    template_name = 'livechat/show.html'
    model = LiveChat

    def get_context_data(self, **kwargs):
        context = super(LiveChatDetailView, self).get_context_data(**kwargs)
        return context
