# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.utils import unittest
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from jmbo.models import ModelBase
from category.models import Category

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

        # create categories for livechat content types
        self.askmama_cat = Category.objects.create(title='Ask MAMA',
                                                   slug='ask-mama')
        self.askmama_cat.save()
        self.livechat_cat = Category.objects.create(title='Live Chat',
                                                    slug='live-chat')
        self.livechat_cat.save()

    def tearDown(self):
        self.boss_man.delete()
        self.askmama_cat.delete()
        self.livechat_cat.delete()

    def test_livechat(self):
        """ Test a livechat hanging off another content type.
        """
        # create a dummy content type object for the livechat to hang off
        stuff = DummyContentType(title="Dummy Content",
                                 slug='dummy-content')
        stuff.state = 'published'
        stuff.owner = self.boss_man
        stuff.save()

        # create the live chat
        now = datetime.now()
        chat = LiveChat.objects.create(content_object=stuff,
                                       title="Test Live Chat",
                                       slug='test-live-chat',
                                       chat_starts_at=now-timedelta(hours=1),
                                       chat_ends_at=now+timedelta(hours=1))
        chat.state = 'published'
        chat.sites = [Site.objects.get_current()]
        chat.primary_category = self.askmama_cat
        chat.categories = [self.livechat_cat]
        chat.save()

        stuff_type = ContentType.objects.get_for_model(stuff)
        chats = LiveChat.objects.filter(content_type__pk=stuff_type.id,
                                        object_id=stuff.id)
        self.assertEquals(chat, chats[0])

    def test_upcoming_chat(self):
        """ Test upcoming chats, as in the advertisement banner.
        """
        # 1. Test a chat in the past
        now = datetime.now()
        chat = LiveChat.objects.create(title="Test Live Chat",
                                       slug='test-live-chat',
                                       chat_starts_at=now-timedelta(hours=2),
                                       chat_ends_at=now-timedelta(hours=1))
        chat.state = 'published'
        chat.sites = [Site.objects.get_current()]
        chat.primary_category = self.askmama_cat
        chat.categories = [self.livechat_cat]
        chat.save()
        upcoming = LiveChat.chat_finder.upcoming_live_chat()
        self.assertIsNone(upcoming)

        # 2. Test a chat in the future
        chat.chat_starts_at = now + timedelta(hours=1)
        chat.chat_ends_at = now + timedelta(hours=2)
        chat.save()
        upcoming = LiveChat.chat_finder.upcoming_live_chat()
        self.assertEquals(upcoming, chat)

        # 3. Test a chat that is currently in progress
        chat.chat_starts_at = now - timedelta(hours=1)
        chat.save()
        current = LiveChat.chat_finder.upcoming_live_chat()
        self.assertEquals(current, chat)

    def test_current_chat(self):
        """ Test chats in progress
        """
        # 1. Test a chat in the past
        now = datetime.now()
        chat = LiveChat.objects.create(title="Test Live Chat",
                                       slug='test-live-chat',
                                       chat_starts_at=now-timedelta(hours=2),
                                       chat_ends_at=now-timedelta(hours=1))
        chat.state = 'published'
        chat.sites = [Site.objects.get_current()]
        chat.primary_category = self.askmama_cat
        chat.categories = [self.livechat_cat]
        chat.save()
        past_chat = LiveChat.chat_finder.get_current_live_chat()
        self.assertIsNone(past_chat)

        # 2. Test a chat in the future
        chat.chat_starts_at = now + timedelta(hours=1)
        chat.chat_ends_at = now + timedelta(hours=2)
        chat.save()
        upcoming = LiveChat.chat_finder.get_current_live_chat()
        self.assertIsNone(upcoming)

        # 3. Test a chat that is currently in progress
        chat.chat_starts_at = now - timedelta(hours=1)
        chat.save()
        current = LiveChat.chat_finder.get_current_live_chat()
        self.assertEquals(current, chat)
