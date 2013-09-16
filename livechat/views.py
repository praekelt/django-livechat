from django.views.generic.base import TemplateView


class LiveChatDetailView(TemplateView):
    template_name = 'livechat/show.html'
