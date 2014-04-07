# -*- coding: utf-8 -*-

from django.test import TestCase
from model_mommy import mommy
import mox

from hubs.models import (
    Hub, HubUser, HubOwner, HubQueryset, HubManager, USER_MODEL)


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
            map(repr, [self.good1, self.good2, self.private]), ordered=False)

    def test_disabled(self):
        query = self.qs.disabled()
        self.assertQuerysetEqual(
            query, map(repr, [self.banned1, self.banned2]), ordered=False)

    def test_private(self):
        query = self.qs.private()
        self.assertQuerysetEqual(
            query, map(repr, [self.private, self.banned2]), ordered=False)

    def test_public(self):
        query = self.qs.public()
        self.assertQuerysetEqual(
            query, map(repr, [self.good1, self.good2]), ordered=False)

    def test_get_for_user(self):
        query = self.qs.get_for_user(self.user)
        self.assertQuerysetEqual(
            query,
            map(repr, [self.good1, self.private, self.banned2]), ordered=False)

