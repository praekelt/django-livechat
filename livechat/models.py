from datetime import datetime, timedelta

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import comments

from jmbo.managers import PermittedManager
from jmbo.models import ModelBase


Comment = comments.get_model()


class LiveChatManager(PermittedManager):
    """ Model manager for live chat models. Used to find any upcoming live
        chats.
    """

    def upcoming_live_chat(self):
        """
        Find any upcoming or current live chat to advertise on the home page or
        live chat page. 
        These are LiveChat's with primary category of 'ask-mama' and category of
        'live-chat'. The Chat date must be less than 5 days away, or happening
        now.
        """
        chat = None
        now = datetime.now()
        advert_window_start = now - timedelta(days=5)

        lcqs = self.get_query_set()
        lcqs = lcqs.filter(
            primary_category__slug='ask-mama',
            categories__slug='live-chat',
            chat_starts_at__gte=advert_window_start,
            chat_ends_at__gte=now).order_by('-chat_starts_at')
        if lcqs.exists():
            chat = lcqs.latest('chat_starts_at')

        return chat

    def get_current_live_chat(self):
        """ Check if there is a live chat on the go, so that we should take over
            the AskMAMA page with the live chat.
        """
        now = datetime.now()
        chat = self.upcoming_live_chat()
        if chat and chat.is_in_progress():
            return chat
        return None


class LiveChat(ModelBase):
    """ Defines a live chat model that acts as anchor for a livechat session.
    Participants use Django comments to post questions and comments. An expert
    or moderator can use functionality in the admin site to add responses.

    The live chat can be uses as a stand-alone object instance, or use a generic
    foreign key mechanism to attach to another content type in the Django site.

    Template tags are provided to display the chat in place in the site.
    """
    # Use a generic foreign key mechanism to be able to link livechats to any
    # content type.
    # content_type = already exists in ModelBase
    object_id = models.PositiveIntegerField(
        null=True, blank=True,
        editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    chat_starts_at = models.DateTimeField(
        help_text="Date and time on which the chat will open for questions.")
    chat_ends_at = models.DateTimeField(
        help_text="Date and time on which the chat will close.")

    objects = models.Manager()
    chat_finder = LiveChatManager()

    class Meta:
        ordering = ['-chat_starts_at', '-created']
        verbose_name = 'Live Chat'
        verbose_name_plural = 'Live Chats'

    def __unicode__(self):
        return 'Live Chat %s' % (self.title,)

    def comment_set(self):
        """ Get the comments that have been submitted for the chat
        """
        ct = ContentType.objects.get_for_model(self.__class__)
        qs = Comment.objects.filter(
            content_type=ct,
            object_pk=self.pk)
        qs = qs.exclude(is_removed=True)
        qs = qs.order_by('-submit_date')
        return qs

    def is_in_progress(self):
        """ Check if the chat is currently in progress
        """
        now = datetime.now()
        return now > self.chat_starts_at and now <= self.chat_ends_at


class LiveChatResponse(models.Model):
    """ This is a response to a live chat comment or question. This response is
    created in the admin site by an expert or moderator.
    """
    livechat = models.ForeignKey(LiveChat)
    author = models.ForeignKey('auth.User')
    comment = models.ForeignKey(Comment)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __unicode__(self):
        return "Live Chat Response from %s: %s" % (self.author,
                                                   self.response[:50])
