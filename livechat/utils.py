from models import LiveChat


def test_close_chat(chat_id):
    chat = LiveChat.objects.get(pk=chat_id)
    if chat.comment_set().count >= int(chat.maximum_questions)-1:
        chat.comments_closed = True
        chat.save()
    return chat


def cancel_chat(chat_id):
    chat = LiveChat.objects.get(pk=chat_id)
    chat.is_cancelled = True
    chat.save()
    return chat