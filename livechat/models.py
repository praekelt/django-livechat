from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import comments


Comment = comments.get_model()


class SiteManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        qs = super(SiteManager, self).get_query_set(*args, **kwargs)
        return qs.filter(sites=Site.objects.get_current(), published=True)


class LiveChat(models.Model):
    # Use a generic foreign key mechanism to be able to link livechats to any
    # content type.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    published = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    sites = models.ManyToManyField(Site)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    site = SiteManager()

    class Meta:
        ordering = ['-published', '-created_at']

    def comment_set(self):
        ct = ContentType.objects.get_for_model(self.__class__)
        return Comment.objects.filter(content_type=ct, object_pk=self.pk).order_by('-submit_date')

    def __unicode__(self):
        return 'Live Chat %s' % (self.title,)

class LiveChatResponse(models.Model):
    livechat = models.ForeignKey(LiveChat)
    author = models.ForeignKey('auth.User')
    comment = models.ForeignKey(Comment,
            limit_choices_to={'object_pk':livechat})
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __unicode__(self):
        return "Live Chat Response from %s: %s" % (self.author,
            self.response[:50])
