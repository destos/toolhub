from django.test.client import RequestFactory
from django.test import TestCase
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from model_mommy import mommy
import mox

from toolhub.mixins import RestrictToUserMixin


class NewView(RestrictToUserMixin, SingleObjectMixin, View):
    pass


class RestrictToUserMixinTest(TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.view = NewView()
        self.view.request = RequestFactory().get('')
        self.user = mommy.make('auth.User', is_staff=False, is_active=True)
        self.view.request.user = self.user

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_attr(self):
        self.assertEqual(self.view.restrict_user_field, 'user')

    def test_filter(self):
        self.mox.StubOutWithMock(SingleObjectMixin, 'get_queryset')
        qs = self.mox.CreateMockAnything()
        qs.filter(user=self.user)
        SingleObjectMixin.get_queryset().AndReturn(qs)
        self.mox.ReplayAll()
        self.view.get_queryset()
        self.mox.VerifyAll()

    def test_change_filter_field(self):
        self.view.restrict_user_field = 'tool_owner'
        self.mox.StubOutWithMock(SingleObjectMixin, 'get_queryset')
        qs = self.mox.CreateMockAnything()
        qs.filter(tool_owner=self.user)
        SingleObjectMixin.get_queryset().AndReturn(qs)
        self.mox.ReplayAll()
        self.view.get_queryset()
        self.mox.VerifyAll()
