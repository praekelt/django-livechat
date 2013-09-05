from django.shortcuts import render
from django.contrib import admin
from django.core.paginator import Paginator
from django import forms

from livechat.models import LiveChat, LiveChatResponse


class LiveChatAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LiveChatAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LiveChat


class LiveChatAdmin(admin.ModelAdmin):
    form = LiveChatAdminForm

    list_filter = ['published', 'active', 'sites', 'created_at']
    list_display = ['title', 'active']
    fields = (
        'published',
        'active',
        'title',
        'description',
        'sites',
    )
    
    def has_add_permission(self, request):
        """ We will be adding livechats where it is needed by declaring an
        inline admin model for it for the relevant content type. For an example,
        see the AskMAMA project's mama/admin.py module.
        """
        return False

    def get_urls(self):
        urls = super(LiveChatAdmin, self).get_urls()
        from django.conf.urls.defaults import patterns
        my_urls = patterns('',
            (r'^(?P<pk>\d+)/participate/$', 
                self.admin_site.admin_view(self.participate), 
                {}, 
                "livechat"),
            (r'^(?P<pk>\d+)/participate_responses/$', 
                self.admin_site.admin_view(self.participate_responses), 
                {}, 
                "participate_responses"),
        )
        return my_urls + urls

    def participate(self, request, pk):
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
