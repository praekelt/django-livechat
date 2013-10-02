from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from livechat.models import LiveChat


class LiveChatDetailView(TemplateView):
    template_name = 'livechat/show.html'


class LiveChatArchiveView(DetailView):
    template_name = 'livechat/archived_chat.html'

    def get_context_data(self, **kwargs):
        context = super(LiveChatArchiveView, self).get_context_data(**kwargs)
        request = self.request
        try:
            paginator = Paginator(
                self.object.comment_set(),
                per_page=10)
            context['chat_comments'] = paginator.page(request.GET.get('p', 1))
        except (KeyError, AttributeError):
            pass
        return context 

    def get_object(self):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        return get_object_or_404(LiveChat, slug=slug)
