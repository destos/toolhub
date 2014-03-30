from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey


class ToolClassification(MPTTModel):
    """High level classification of a tool"""
    name = models.CharField(max_length=255, unique=True, blank=False)
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children')
    slug = AutoSlugField(populate_from='name')

    class MPTTMeta:
        order_insertion_by = ['name']

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
