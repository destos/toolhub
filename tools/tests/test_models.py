from django.conf import settings
from django.test import TestCase
from model_mommy import mommy
import mox

from test_app.utils import models_to_query
from tools import models


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ToolClassificationManagerTest(TestCase):
    def test_published(self):
        pass

    def test_filtered(self):
        pass


class ToolClassificationTest(TestCase):
    pass


class ToolQuerySetTest(TestCase):
    def setUp(self):
        self.qs = models.ToolQuerySet()

    def test_children_tools(self):
        top = mommy.make(models.ToolClassification)
        mid1 = mommy.make(models.ToolClassification, parent=top)
        mid2 = mommy.make(models.ToolClassification, parent=top)
        bottom = mommy.make(models.ToolClassification, parent=mid1)

        top_tool = mommy.make(models.Tool, parent=top)
        mid1_tool = mommy.make(models.Tool, parent=mid1)
        mid2_tool = mommy.make(models.Tool, parent=mid2)
        bottom_tool = mommy.make(models.Tool, parent=bottom)

        query = self.qs.children_tools(top)
        self.assertQuerysetEqual(
            query,
            models_to_query(top_tool, mid1_tool, mid2_tool, bottom_tool),
            ordered=False)

        query = self.qs.children_tools(mid1)
        self.assertQuerysetEqual(
            query,
            models_to_query(mid1_tool, bottom_tool), ordered=False)

        query = self.qs.children_tools(bottom)
        self.assertQuerysetEqual(
            query, models_to_query(bottom_tool), ordered=False)

        query = self.qs.children_tools(mid2)
        self.assertQuerysetEqual(
            query, models_to_query(mid2_tool), ordered=False)

    def test_tools_from_users(self):
        user = mommy.make(USER_MODEL)
        another_user = mommy.make(USER_MODEL)

        tool_class = mommy.make(models.ToolClassification)
        tool = mommy.make(models.Tool, parent=tool_class)
        another_tool = mommy.make(models.Tool, parent=tool_class)
        mommy.make(models.UserTool, owner=user, tool_type=tool)
        mommy.make(models.UserTool, owner=another_user, tool_type=another_tool)
        mommy.make(models.UserTool, owner=another_user, tool_type=another_tool)
        mommy.make(models.UserTool, owner=another_user, tool_type=tool)

        query = self.qs.tools_from_users([user])
        self.assertQuerysetEqual(
            query, models_to_query(tool), ordered=False)

    def test_published(self):
        pass


class ToolManagerTest(TestCase):
    pass


class ToolTest(TestCase):
    pass


class UserToolTest(TestCase):
    def test_new_tool(self):
        """Create a new UserTool with passed in tool type and user"""
        pass
