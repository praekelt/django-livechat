from django.shortcuts import render
from django.contrib import admin
from django.core.paginator import Paginator
from django import forms

from jmbo.admin import ModelBaseAdmin

from livechat.models import LiveChat, LiveChatResponse


class LiveChatAdmin(ModelBaseAdmin):
    # list_display = ['title', 'slug', 'created', 'state']
    # fields = (
    #     'title',
    #     'subtitle',
    #     'description',
    #     'publish_on',
    #     'retract_on',
    #     'primary_category',
    #     'categories',
    #     'comments_closed',
    #     'likes_closed',
    #     'sites'
    # )
    # fieldsets = {}

    change_form_template = 'admin/livechat/livechat/change_form.html'
    
    def get_urls(self):
        urls = super(LiveChatAdmin, self).get_urls()
        from django.conf.urls.defaults import patterns
        my_urls = patterns('',
            (r'^participate_livechat/(?P<pk>\d+)/$', 
                self.admin_site.admin_view(self.participate_livechat), 
                {}, "participate_livechat"),
            (r'^participate_responses/(?P<pk>\d+)/$', 
                self.admin_site.admin_view(self.participate_responses), 
                {}, "participate_responses"),
        )
        return my_urls + urls

    def participate_livechat(self, request, pk):
        livechat = LiveChat.objects.get(pk=pk)
        comments_qs = livechat.comment_set()

        answered = request.GET.get('answered', '')
        popular = request.GET.get('popular', '')
        if answered == 'true':
            comments_qs = comments_qs.filter(livechatresponse__isnull=False)
        if answered == 'false':
            comments_qs = comments_qs.filter(livechatresponse__isnull=True)
        if popular == 'true':
            comments_qs = comments_qs.order_by('-like_count')

        paginator = Paginator(comments_qs, 100)
        comments = paginator.page(request.GET.get('p', 1))
        return render(request, "admin/livechat/livechat/participate.html", {
            'app_label': 'livechat',
            'module_name': 'livechat',
            'livechat': livechat,
            'comments': comments,
            'paginator': paginator,
            'title': 'Participate in %s' % (livechat.title,)
        })

    def participate_responses(self, request, pk):
        try:
            livechat = LiveChat.objects.get(pk=pk)
            comment = livechat.comment_set().get(
                pk=request.GET.get('comment_id'))
        except Comment.DoesNotExist, e:
            comment = None
        except ObjectDoesNotExist, e:
            comment = None

        return render(request, 
                      "admin/livechat/livechat/participate_responses.html", 
                      {
                          'comment': comment
                      })


class LiveChatResponseAdmin(admin.ModelAdmin):
    raw_id_fields = ['comment', 'livechat']
    exclude = ['author']
    list_display = ['comment', 'response']

    fieldsets = (
        (None, {
            'fields': ('comment', 'response', 'livechat',),
        }),
        )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(LiveChat, LiveChatAdmin)
admin.site.register(LiveChatResponse, LiveChatResponseAdmin)
