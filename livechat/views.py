from django.shortcuts import render, get_object_or_404
from django.contrib.sites.models import Site
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

from livechat.models import LiveChat

current_site = Site.objects.get_current()


def show_livechat(request, slug):
    livechat = get_object_or_404(LiveChat, slug=slug, sites=current_site)
    return render(request, 'livechat/show.html', {
        'livechat': livechat,
        'current_url': reverse('livechat:show_livechat', kwargs={
            'slug': livechat.slug,
        })
    })
