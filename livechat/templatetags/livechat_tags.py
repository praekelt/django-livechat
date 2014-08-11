from copy import copy

from django import template
from django.core.paginator import Paginator
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from livechat.models import LiveChat

current_site = Site.objects.get_current()

register = template.Library()


@register.inclusion_tag('livechat/inclusion_tags/live_chat_banner.html',
                        takes_context=True)
def live_chat_banner(context):
    """ Display any available live chats as advertisements.
    """
    context = copy(context)

    # Find any upcoming or current live chat. The Chat date must be less than 5
    # days away, or currently in progress.

    oldchat = LiveChat.chat_finder.get_last_live_chat()

    if oldchat:
        context['last_live_chat'] = {
            'title': oldchat.title,
            'chat_ends_at': oldchat.chat_ends_at,
            'expert': oldchat.expert,
            'url': reverse('livechat:show_archived_livechat')

        }

    chat = LiveChat.chat_finder.upcoming_live_chat()
    if chat is not None:
        context['live_chat_advert'] = {
            'title': chat.title,
            'description': chat.description,
            'expert': chat.expert,
            'commenting_closed': chat.comments_closed,
            'cancelled': chat.is_cancelled,
            'archived': chat.is_archived,
            'in_progress': chat.is_in_progress(),
            'url':  reverse(
                'livechat:show_livechat',
                kwargs={
                    'slug': chat.slug}),
            'archive_url':reverse('livechat:show_archived_livechat')

        }
        context['live_chat_advert']['datetime'] = {
            'time': chat.chat_starts_at.time,
            'date': chat.chat_starts_at.date
            }
    return context


@register.inclusion_tag('livechat/inclusion_tags/live_chat.html',
                        takes_context=True)
def show_live_chat(context):
    context = copy(context)
    request = context['request']

    chat = LiveChat.chat_finder.upcoming_live_chat()
    context['live_chat'] = chat
    context['can_comment'] = chat.is_in_progress()

    try:
        paginator = Paginator(
            context['live_chat'].comment_set(),
            per_page=10)
        context['chat_comments'] = paginator.page(request.GET.get('p', 1))
        context['commenting_closed'] = chat.comments_closed
    except (KeyError, AttributeError):
        pass

    return context


@register.simple_tag(takes_context=True)
def get_livechat_for_article(context, post, var_name):
    post_type = ContentType.objects.get_for_model(post.__class__)
    chats = LiveChat.permitted.filter(content_type=post_type,
                                      object_id=post.id)
    try:
        context[var_name] = chats.latest('created')
    except LiveChat.DoesNotExist:
        pass
    return ''


@register.inclusion_tag('livechat/inclusion_tags/last_live_chat_banner.html',
                        takes_context=True)
def archive_live_chat(context):
    context = copy(context)
    context['url'] = reverse('livechat:show_archived_livechat')
    return context
