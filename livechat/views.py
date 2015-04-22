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
        livechats = LiveChat.objects.all().order_by('-chat_ends_at')

        request = self.request
        try:
            paginator = Paginator(
                livechats,
                per_page=1)
            context['livechats'] = paginator.page(request.GET.get('p', 1))
        except (KeyError, AttributeError):
            pass
        return context

    def get_object(self):
        return LiveChat.objects.filter(is_cancelled=False)
