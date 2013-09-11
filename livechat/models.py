from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import comments

from jmbo.models import ModelBase


Comment = comments.get_model()


class LiveChat(ModelBase):
    # Use a generic foreign key mechanism to be able to link livechats to any
    # content type.
    # content_type = already exists in ModelBase
    object_id = models.PositiveIntegerField(
        null=True, blank=True,
        editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = models.Manager()

    class Meta:
        ordering = ['-publish_on', '-created']
        verbose_name = 'Live Chat'
        verbose_name_plural = 'Live Chats'

    def comment_set(self):
        ct = ContentType.objects.get_for_model(self.__class__)
        return Comment.objects.filter(
            content_type=ct,
            object_pk=self.pk).order_by('-submit_date')

    def __unicode__(self):
        return 'Live Chat %s' % (self.title,)


class LiveChatResponse(models.Model):
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
