from django import template
from django.core.paginator import Paginator
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

# from jmbocomments.models import UserComment, UserCommentFlag
from livechat.models import LiveChat

current_site = Site.objects.get_current()

register = template.Library()


@register.simple_tag(takes_context=True)
def get_livechat_for_article(context, post, var_name):
    post_type = ContentType.objects.get_for_model(post)
    chats = LiveChat.objects.filter(content_type=post_type,
                                    object_id=post.id)
    context[var_name] = chats.latest('created_at')
    return ''

@register.simple_tag(takes_context=True)
def get_livechat_page(context, livechat, var_name):
    """
    Fetches a page object for the given livechat

    Usage:
    {% get_livechat_page `livechat` `var_name` %}
    """
    request = context['request']

    comments_qs = livechat.comment_set().exclude(is_removed=True)
    # comments_qs = comments_qs.exclude(
    #         flag_set__flag=UserCommentFlag.COMMUNITY_REMOVAL)
    # comments_qs = comments_qs.exclude(
    #         flag_set__flag=UserCommentFlag.MODERATOR_DELETION)
    comments_qs = comments_qs.distinct().select_related('user')
    comments_qs = comments_qs.order_by('-submit_date')

    answered = request.GET.get('answered', '')
    popular = request.GET.get('popular', '')
    if answered == 'true':
        comments_qs = comments_qs.filter(livechatresponse__isnull=False)
    if answered == 'false':
        comments_qs = comments_qs.filter(livechatresponse__isnull=True)
    if popular == 'true':
        comments_qs = comments_qs.order_by('-like_count')

    paginator = Paginator(comments_qs, per_page=10)
    page = paginator.page(request.GET.get('p', 1))
    context['page'] = page
    return ''

@register.simple_tag(takes_context=True)
def get_mylivechat(context, livechat, var_name='my_comments'):
    """
    Fetches user's comments for the given livechat

    Usage:
    {% get_mylivechat `livechat` `var_name` %}
    """
    request = context['request']

    if not request.user.is_authenticated():
        return None

    comments_qs = livechat.comment_set().distinct() \
                    .filter(user=request.user)\
                    .select_related('user').order_by('-submit_date')
    context[var_name] = comments_qs
    return ''
