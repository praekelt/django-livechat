# -*- coding: utf-8 -*-

from datetime import datetime

from django.utils import unittest
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from jmbo.models import ModelBase
from livechat.models import LiveChat, LiveChatResponse


class DummyContentType(ModelBase):
    class Meta:
        proxy = True


class LiveChatTestCase(unittest.TestCase):

    def setUp(self):
        # create an admin user
        self.boss_man = User.objects.create(username='boss',
                                            password='bigsecret')
        self.boss_man.is_active = True
        self.boss_man.is_staff = True
        self.boss_man.is_superuser = True
        self.boss_man.save()

        # create a dummy content type object for the livechat to hang off
        now = datetime.now()
        self.stuff = DummyContentType(title="Dummy Content",
                                      slug='dummy-content')
        self.stuff.state = 'published'
        self.stuff.owner = self.boss_man
        self.stuff.save()

    def test_livechat(self):
        chat = LiveChat.objects.create(content_object=self.stuff,
                                       title="Test Live Chat",
                                       slug='test-live-chat')
        chat.save()

        stuff_type = ContentType.objects.get_for_model(self.stuff)
        chats = LiveChat.objects.filter(content_type__pk=stuff_type.id,
                                        object_id=self.stuff.id)
        self.assertEquals(chat, chats[0])
