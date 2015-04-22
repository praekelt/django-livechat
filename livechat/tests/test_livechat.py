# -*- coding: utf-8 -*-
import os
import pytest

from datetime import datetime, timedelta

from django.utils import unittest
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from jmbo.models import ModelBase
from category.models import Category

from livechat.models import LiveChat


class DummyContentType(ModelBase):

    class Meta:
        proxy = True


class MockRequest(object):
    pass


@pytest.mark.django_db
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

        cur_dir = os.path.abspath(os.path.dirname(__file__))
        self.test_image = os.path.join(cur_dir, 'sample_test_image.jpg')

    def tearDown(self):
        self.boss_man.delete()
        self.askmama_cat.delete()
        self.livechat_cat.delete()

    def test_livechat(self):
        """ Test a livechat hanging off another content type.
        """
        # create a dummy content type object for the livechat to hang off
        stuff = DummyContentType(title="Dummy Content",
                                 image=self.test_image,
                                 slug='dummy-content')
        stuff.state = 'published'
        stuff.owner = self.boss_man
        stuff.save()

        # create the live chat
        now = datetime.now()
        chat = LiveChat.objects.create(content_object=stuff,
                                       title="Test Live Chat",
                                       slug='test-live-chat',
                                       image=self.test_image,
                                       chat_starts_at=now - timedelta(hours=1),
                                       chat_ends_at=now + timedelta(hours=1))
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
                                       image=self.test_image,
                                       chat_starts_at=now - timedelta(hours=2),
                                       chat_ends_at=now - timedelta(hours=1))
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
                                       image=self.test_image,
                                       chat_starts_at=now - timedelta(hours=2),
                                       chat_ends_at=now - timedelta(hours=1))
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

    def test_last_live_chat(self):
        """ Test finding a concluded chat up to 3 days ago, to show an archived
            view of it.
        """
        # 1. Test a chat more than 4 days ago in the past.
        now = datetime.now()
        chat = LiveChat.objects.create(title="Test Live Chat",
                                       slug='test-live-chat',
                                       image=self.test_image,
                                       chat_starts_at=now - timedelta(days=5),
                                       chat_ends_at=now - timedelta(days=4))
        chat.state = 'published'
        chat.sites = [Site.objects.get_current()]
        chat.primary_category = self.askmama_cat
        chat.categories = [self.livechat_cat]
        chat.save()
        past_chat = LiveChat.chat_finder.get_last_live_chat()
        self.assertIsNone(past_chat)

        # 2. Test a chat in the goldilocks range, i.e. ended less than 3 days
        # ago.
        chat.chat_ends_at = now - timedelta(days=2)
        chat.save()
        last_chat = LiveChat.chat_finder.get_last_live_chat()
        self.assertEquals(last_chat, chat)

        # 3. Test a chat that is currently in progress
        chat.chat_starts_at = now - timedelta(hours=1)
        chat.chat_ends_at = now + timedelta(hours=2)
        chat.save()
        current = LiveChat.chat_finder.get_last_live_chat()
        self.assertIsNone(current)

        # 3. Test a future chat
        chat.chat_starts_at = now + timedelta(hours=1)
        chat.chat_ends_at = now + timedelta(hours=2)
        chat.save()
        future = LiveChat.chat_finder.get_last_live_chat()
        self.assertIsNone(future)

    def test_max_questions(self):
        """Test if max_questions method closes commenting"""

        # 1. Create open chat
        now = datetime.now()
        chat = LiveChat.objects.create(title="Test Live Chat",
                                       slug='test-live-chat',
                                       image=self.test_image,
                                       chat_starts_at=now - timedelta(days=1),
                                       chat_ends_at=now - timedelta(days=1),
                                       )

        # 2. Test method doesn't crash if none
        chat.maximum_questions = None
        chat.save()
        chat.check_max_comments()

        # 3. Change max_questions to 0
        chat.maximum_questions = 0
        chat.save()

        # 4. Test commenting closed
        chat.check_max_comments()
        self.assertTrue(chat.comments_closed)

    def test_cancel_chat(self):

        now = datetime.now()
        chat = LiveChat.objects.create(title="Test Live Chat",
                                       slug='test-live-chat',
                                       image=self.test_image,
                                       chat_starts_at=now - timedelta(days=1),
                                       chat_ends_at=now - timedelta(days=1),
                                       maximum_questions=1,
                                       )

        queryset = LiveChat.objects.all()

        for chat in queryset:
            chat.is_cancelled = True
            chat.save()

        self.assertTrue(chat.is_cancelled)
