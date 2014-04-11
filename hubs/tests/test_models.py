# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.utils import override_settings
from django.db import IntegrityError
from model_mommy import mommy
import mox

from hubs.models import (
    Hub, HubUser, HubOwner, HubQueryset, HubManager, PublicHubManager,
    USER_MODEL)
from test_app.utils import models_to_query


class HubQuerysetTests(TestCase):
    def setUp(self):
        # AutoSlugField isn't supported by mommy so
        # default values are provided
        self.good1 = mommy.make(
            'hubs.Hub', is_enabled=True, is_private=False, slug='')
        self.good2 = mommy.make(
            'hubs.Hub', is_enabled=True, is_private=False, slug='')
        self.banned1 = mommy.make(
            'hubs.Hub', is_enabled=False, is_private=False, slug='')
        self.banned2 = mommy.make(
            'hubs.Hub', is_enabled=False, is_private=True, slug='')
        self.private = mommy.make(
            'hubs.Hub', is_enabled=True, is_private=True, slug='')
        self.user = mommy.make(USER_MODEL)
        self.good1.add_user(self.user)
        self.private.add_user(self.user)
        self.banned2.add_user(self.user)

        self.qs = HubQueryset(model=Hub)

    def test_enabled(self):
        query = self.qs.enabled()
        self.assertQuerysetEqual(
            query,
            models_to_query(
                self.good1, self.good2, self.private), ordered=False)

    def test_disabled(self):
        query = self.qs.disabled()
        self.assertQuerysetEqual(
            query, models_to_query(self.banned1, self.banned2), ordered=False)

    def test_private(self):
        query = self.qs.private()
        self.assertQuerysetEqual(
            query, models_to_query(self.private, self.banned2), ordered=False)

    def test_public(self):
        query = self.qs.public()
        self.assertQuerysetEqual(
            query, models_to_query(self.good1, self.good2), ordered=False)

    def test_get_for_user(self):
        query = self.qs.get_for_user(self.user)
        self.assertQuerysetEqual(
            query,
            models_to_query(
                self.good1, self.private, self.banned2), ordered=False)


class HubManagerTest(TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.manager = HubManager()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_get_query_set(self):
        from hubs import models
        self.manager.model = Hub
        self.manager._db = 'db'
        self.mox.StubOutWithMock(models, 'HubQueryset')
        models.HubQueryset(Hub, using='db')
        self.mox.ReplayAll()
        self.manager.get_query_set()
        self.mox.VerifyAll()

    def test_get_for_user(self):

        self.mox.StubOutWithMock(self.manager, 'get_query_set')
        qs_return = self.mox.CreateMockAnything()
        self.manager.get_query_set().AndReturn(qs_return)
        # calls HubQuerySet with passed in user
        qs_return.get_for_user('a-user')
        self.mox.ReplayAll()
        self.manager.get_for_user('a-user')
        self.mox.VerifyAll()


class PublicHubManagerTests(TestCase):
    """
    The public manager only returns Hubs that are enabled and not private,
    so it uses the public method from HubQueryset, which HubManager uses.
    """
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_get_query_set(self):
        self.mox.StubOutWithMock(HubManager, 'get_query_set')
        hub_query_set = self.mox.CreateMockAnything()
        HubManager.get_query_set().AndReturn(hub_query_set)
        # uses public hub queryset method
        hub_query_set.public().AndReturn('qs')
        self.mox.ReplayAll()
        returned = PublicHubManager().get_query_set()
        self.mox.VerifyAll()
        self.assertEqual(returned, 'qs')


class HubModelTests(TestCase):

    def setUp(self):
        self.mox = mox.Mox()
        self.hub = mommy.make(Hub, name='A hub', slug='a-hub')
        self.user1 = mommy.make(USER_MODEL)
        self.user2 = mommy.make(USER_MODEL)

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_string_representation(self):
        self.assertEqual(unicode(self.hub), 'A hub')

    def test_get_absolute_url(self):
        url = self.hub.get_absolute_url()
        self.assertEqual(url, '/hubs/a-hub/')

    def test_get_edit_url(self):
        url = self.hub.get_edit_url()
        self.assertEqual(url, '/hubs/a-hub/edit/')

    def test_add_user(self):
        returned_user1 = self.hub.add_user(self.user1)
        returned_user2 = self.hub.add_user(self.user2)
        self.assertTrue(self.hub.is_admin(self.user1))
        self.assertFalse(self.hub.is_admin(self.user2))
        # sets first user added to hub as owner
        self.assertTrue(self.user1 == self.hub.owner.hub_user.user)
        # returns hub users
        self.assertEqual(self.user1, returned_user1.user)
        self.assertEqual(self.user2, returned_user2.user)

    def test_add_user_admin(self):
        returned_user1 = self.hub.add_user(self.user1, is_admin=True)
        returned_user2 = self.hub.add_user(self.user2, is_admin=True)
        self.assertTrue(self.hub.is_admin(self.user1))
        self.assertTrue(self.hub.is_admin(self.user2))
        # sets first user added to hub as owner
        self.assertTrue(self.user1 == self.hub.owner.hub_user.user)
        # returns hub users
        self.assertEqual(self.user1, returned_user1.user)
        self.assertEqual(self.user2, returned_user2.user)

    def test_add_user_duplicate(self):
        returned_user1 = self.hub.add_user(self.user1)
        self.assertTrue(self.hub.is_admin(self.user1))
        # returns hub users
        self.assertEqual(self.user1, returned_user1.user)
        self.assertRaises(IntegrityError, self.hub.add_user, self.user1)

    def test_get_or_add_user(self):
        returned_user1, created1 = self.hub.get_or_add_user(self.user1)
        returned_user2, created2 = self.hub.get_or_add_user(self.user2)
        self.assertTrue(self.hub.is_admin(self.user1))
        self.assertFalse(self.hub.is_admin(self.user2))
        # sets first user added to hub as owner
        self.assertTrue(self.user1 == self.hub.owner.hub_user.user)
        # returns hub users
        self.assertEqual(self.user1, returned_user1.user)
        self.assertEqual(self.user2, returned_user2.user)
        # created both users
        self.assertTrue(created1 & created2)
        # lookup already added user returns hub user and false created
        returned_user2, created2 = self.hub.get_or_add_user(self.user2)
        self.assertEqual(self.user2, returned_user2.user)
        self.assertFalse(created2)

    def test_get_or_add_user_admin(self):
        returned_user1, created1 = self.hub.get_or_add_user(
            self.user1, is_admin=True)
        returned_user2, created2 = self.hub.get_or_add_user(
            self.user2, is_admin=True)
        self.assertTrue(self.hub.is_admin(self.user1))
        self.assertTrue(self.hub.is_admin(self.user2))
        # sets first user added to hub as owner
        self.assertTrue(self.user1 == self.hub.owner.hub_user.user)
        # returns hub users
        self.assertEqual(self.user1, returned_user1.user)
        self.assertEqual(self.user2, returned_user2.user)
        # created both users
        self.assertTrue(created1 & created2)
        # lookup already added user returns hub user and false created
        returned_user2, created2 = self.hub.get_or_add_user(self.user2)
        self.assertEqual(self.user2, returned_user2.user)
        self.assertFalse(created2)

    def test_user_count(self):
        self.assertEqual(self.hub.user_count, 0)
        self.hub.add_user(self.user1)
        self.hub.add_user(self.user2)
        self.assertEqual(self.hub.user_count, 2)

    def test_is_member(self):
        self.hub.add_user(self.user1)
        self.assertTrue(self.hub.is_member(self.user1))
        self.assertFalse(self.hub.is_member(self.user2))

    def test_is_admin(self):
        self.hub.add_user(self.user1, is_admin=True)
        self.assertTrue(self.hub.is_admin(self.user1))

    def test_delete_owner(self):
        from hubs.exceptions import OwnershipRequired
        owner = self.hub.add_user(self.user1)
        self.assertRaises(OwnershipRequired, owner.delete)

    def test_delete_missing_owner(self):
        """Ensure an org user can be deleted when there is no owner"""
        # Avoid the Hub.add_user method which would make an owner
        hub_user = mommy.make(HubUser, user=self.user1, hub=self.hub)
        # Just make sure it doesn't raise an error
        hub_user.delete()

    def test_nonmember_owner(self):
        from hubs.exceptions import HubMismatch
        other_hub = mommy.make(
            Hub, slug='other-hub', hub_owner__hub_user__user=self.user1)
        # other_hub_owner = mommy.make(
        #     HubUser, hub=other_hub, )
        self.hub.owner = other_hub.owner
        self.assertRaises(HubMismatch, self.hub.owner.save)


# @override_settings(USE_TZ=True)
# class HubDeleteTests(TestCase):

#     fixtures = ['users.json', 'hubs.json']

#     def test_delete_account(self):
#         """Ensure Users are not deleted on the cascade"""
#         self.assertEqual(3, HubOwner.objects.all().count())
#         self.assertEqual(4, User.objects.all().count())
#         scream = Hub.objects.get(name="Scream")
#         scream.delete()
#         self.assertEqual(2, HubOwner.objects.all().count())
#         self.assertEqual(4, User.objects.all().count())

#     def test_delete_hubuser(self):
#         """Ensure the user is not deleted on the cascade"""
#         krist = User.objects.get(username="krist")
#         hub_user = HubUser.objects.filter(
#                 hub__name="Nirvana", user=krist)
#         hub_user.delete()
#         self.assertTrue(krist.pk)
