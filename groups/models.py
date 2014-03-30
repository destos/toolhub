from django.db import models
from django_extents.db.models import TimeStampedModel


class LocalGroup(TimeStampedModel):
	"""Handles relations to different users and their shared tools"""
