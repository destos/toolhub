from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from mptt.models import MPTTModel, TreeManager, TreeForeignKey

from lending.models import LendingAction


class ToolClassificationManager(TreeManager):
    def published(self):
        return self.get_query_set().filter(status=ToolClassification.PUBLISHED)

    def filtered(self):
        return self.get_query_set().exclude(status=ToolClassification.BANNED)


class ToolClassification(MPTTModel):
    """High level classification of a tool"""
    name = models.CharField(max_length=255, unique=True, blank=False)
    slug = AutoSlugField(populate_from='name', max_length=255, unique=True)
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children')
    order = models.IntegerField(blank=False, default=0)
    # locked categories can't be moved or edited.
    locked = models.BooleanField(default=False)

    # TODO: use model utils status
    IN_REVIEW = 0
    PUBLISHED = 1
    BANNED = 2
    STATUS_CHOICES = (
        (IN_REVIEW, 'in review'), (PUBLISHED, 'published'), (BANNED, 'banned'))
    status = models.IntegerField(choices=STATUS_CHOICES, default=IN_REVIEW)
    # Add a relation to similar classifications?

    objects = ToolClassificationManager()

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        verbose_name_plural = 'Tool Classifications'

    def __unicode__(self):
        return self.name

    @permalink
    def get_list_url(self):
        pass

    def get_absolute_url(self):
        return reverse('tools:list_class',
                       kwargs=dict(tool_class_slug=self.slug))


class ToolQuerySet(models.query.QuerySet):
    def children_tools(self, tool_class):
        """
        Children tools are all tools that are related to the current tool class
        node and it's children.
        """
        # TODO: check for being instance of ToolClassification
        # This probably can be solved with mptt
        children = [child.id for child in tool_class.get_children()]
        children.append(tool_class.id)
        return self.filter(parent__in=children)

    def tools_from_users(self, users):
        return self.filter(user_tools__owner__in=users)

    def published(self):
        return self.filter(published=True)


class ToolManager(models.Manager):
    def get_query_set(self):
        return ToolQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_query_set().published()

    def tools_from_users(self, users):
        return self.get_query_set().tools_from_users(users)

    def children_tools(self, tool_class):
        return self.get_query_set().children_tools(tool_class)


# Specific tool types
class Tool(models.Model):
    """
    Describes a specific tool in greater detail
    """
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', max_length=255, unique=True)
    description = models.TextField(blank=True)
    model_number = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    classifications = models.ManyToManyField(
        ToolClassification, related_name='tools', blank=False)
    # TODO: rename to category, change proper mptt settings
    parent = TreeForeignKey(ToolClassification)
    # TODO: used_with relationships, parts of tool
    # TODO: convert these to localized fields
    value = models.FloatField(default=3.50, help_text='monetary value')
    weight = models.FloatField(default=0.0, help_text='weight in grams')
    published = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User, blank=True, null=True, default=None,
        related_name='suggested_tools')

    objects = ToolManager()

    def __unicode__(self):
        return self.name

    def main_class(self):
        # TODO: do this mo-better
        return self.parent

    def get_absolute_url(self):
        return reverse('tools:detail',
                       kwargs=dict(tool_slug=self.slug))


class UserTool(models.Model):
    # Does the user have a nickname for the tool?
    callsign = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=_('your nickname for the tool'))
    tool_type = models.ForeignKey(
        Tool, related_name='user_tools', blank=True, null=False, default=None)
    owner = models.ForeignKey(
        User, blank=False, null=False, default=None, related_name='tools')
    # instructions = models.ForeignKey('UserToolInstructions', blank=True)

    # currently quality or workability of tool?
    # details on the desired portability of the tool
    PICKUP = 0
    DROP_OFF = 1
    ON_LOCATION = 2
    PORT_CHOICES = (
        (PICKUP, _('can pickup')), (DROP_OFF, _('dropped off')),
        (ON_LOCATION, _('can use on premisis')))
    portability = models.IntegerField(
        choices=PORT_CHOICES,
        default=PICKUP,
        help_text=_('where the tool can be used'))

    def __unicode__(self):
        return u"%s's %s" % (self.owner, self.display_name,)

    @property
    def display_name(self):
        return self.callsign or self.tool_type.name

    def get_latest_lending_action(self):
        """
        Returns the current lending state this user's tool is in.
        States can be then looked on in lending.models.
        """
        return self.lending_transactions.latest(
            'created').history.latest('created')

    @property
    def lent(self):
        return self.get_latest_lending_action().action not in (
            LendingAction.CLOSING_ACTIONS)


# class UserToolInstructions(models.Model):
#     pass
