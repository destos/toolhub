from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import AutoSlugField
from mptt.models import MPTTModel, TreeManager, TreeForeignKey


class ToolClassificationManager(TreeManager):
    def published(self):
        return self.get_query_set().filter(status=ToolClassification.PUBLISHED)


class ToolClassification(MPTTModel):
    """High level classification of a tool"""
    name = models.CharField(max_length=255, unique=True, blank=False)
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children')
    slug = AutoSlugField(populate_from='name', max_length=255, unique=True)
    order = models.IntegerField(blank=False, default=0)
    # locked categories can't be moved or edited.
    locked = models.BooleanField(default=False)

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


class Tool(models.Model):
    """Describes a specific tool in greater detail"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    model_number = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    classifications = models.ManyToManyField(
        ToolClassification, related_name='tools', blank=False)
    # used_with relationships, part of tool
    # monetary value
    value = models.FloatField(default=3.50)
    # weight in grams
    weight = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.name


class UserTool(models.Model):
    # Does the user have a nickname for the tool?
    callsign = models.CharField(max_length=255, blank=True, null=True)
    tool_type = models.ForeignKey(
        Tool, related_name='user_tools', blank=False, null=False, default=None)
    owner = models.ForeignKey(
        User, blank=False, null=False, default=None, related_name='tools')

    # currently quality or workability of tool?
    # details on the desired portability of the tool
    PICKUP = 0
    DROP_OFF = 1
    ON_LOCATION = 2
    PORT_CHOICES = (
        (PICKUP, 'can pickup'), (DROP_OFF, 'dropped off'),
        (ON_LOCATION, 'use on premisis'))
    portability = models.IntegerField(
        choices=PORT_CHOICES, default=PICKUP)

    def __unicode__(self):
        return u'%s\'s %s' % (
            self.owner, (self.callsign or self.tool_type.name))
