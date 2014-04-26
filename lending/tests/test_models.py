from django.test import TestCase
from model_mommy import mommy
import mox

from tools.models import Tool
from lending.models import Transaction, LendingAction


class TestLendingAction(TestCase):
    def setUp(self):
        # ToolClassification.object.create
        self.tool = mommy.make(Tool)
        self.transaction = mommy.make(Transaction, tool=self.tool)
        self.action = mommy.make(LendingAction)
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_unicode(self):
        self.mox.StubOutWithMock(self.action, 'action_text')
        self.action.action_text().AndReturn('action_text')
        self.mox.StubOutWithMock(self.transaction.tool, '__unicode__')
        self.mox.StubOutWithMock(self.transaction.lendee, '__unicode__')
        self.transaction.tool.__unicode__().AndReturn('tool_unicode')
        self.transaction.lendee.__unicode__().AndReturn('lendee_unicode')
        self.mox.ReplayAll()
        self.assertEqual(
            str(self.action), 'action_text, tool_unicode to lendee_unicode')
        self.mox.VerifyAll()

    def test_lending_choices(self):
        pass

    def test_action_key(self):
        pass

    def test_action_text(self):
        pass


class TestTransaction(TestCase):
    def setUp(self):
        self.model = mommy.make(Transaction)
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_unicode(self):
        self.assertEqual(
            str(self.model), 'tool_type, tool_owner to lendee')

    def test_lender_property(self):
        self.assertEqual(self.model.lender, self.tool.owner)

    def test_closed_property(self):
        self.mox.StubOutWithMock(self.model, 'get_closing_action')
        closing_action_return_qs = self.mox.CreateMockAnything()
        self.model.get_closing_action().AndReturn(closing_action_return_qs)
        closing_action_return_qs.exists().AndReturn(True)

        self.mox.ReplayAll()
        self.assertTrue(self.model.closed)
        self.mox.VerifyAll()

    def test_get_closing_action_no_actions(self):
        # Don't create history item models
        closing_action = self.model.get_closing_action()
        pass

    def test_get_closing_action_has_actions(self):
        # Create history item models
        closing_action = self.model.get_closing_action()
        pass
