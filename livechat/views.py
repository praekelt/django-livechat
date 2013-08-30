from django.shortcuts import render, get_object_or_404
from django.contrib.sites.models import Site
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

from livechat.models import LiveChat

current_site = Site.objects.get_current()


def index(request):
    paginator = Paginator(LiveChat.site.all(), per_page=8)
    page = paginator.page(request.GET.get('p', 1))
    return render(request, 'livechat/index.html', {
        'paginator': paginator,
        'page': page,
    })


def show(request, pk):
    livechat = get_object_or_404(LiveChat, pk=pk, sites=current_site)
    return render(request, 'livechat/show.html', {
        'livechat': livechat,
        'current_url': reverse('livechat:show', kwargs={
            'pk': livechat.pk,
        })
    })
