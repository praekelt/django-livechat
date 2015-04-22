from livechat.models import LiveChat


def current_livechat(request):
    """
    Checks if a live chat is currently on the go, and add it to the request
    context.

    This is to allow the AskMAMA URL in the top-navigation to be redirected to
    the live chat object view consistently, and to make it available to the
    views and tags that depends on it.
    """
    result = {}
    livechat = LiveChat.chat_finder.get_current_live_chat()
    if livechat:
        result['live_chat'] = {}
        result['live_chat']['current_live_chat'] = livechat
        can_comment, reason_code = livechat.can_comment(request)
        result['live_chat']['can_render_comment_form'] = can_comment
        result['live_chat']['can_comment_code'] = reason_code
    return result
