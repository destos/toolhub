# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, blank=True, unique=True)),
                ('description', models.TextField(blank=True)),
                ('model_number', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('value', models.FloatField(default=3.5, help_text=b'monetary value')),
                ('weight', models.FloatField(default=0.0, help_text=b'weight in grams')),
                ('published', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ToolClassification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, blank=True, unique=True)),
                ('order', models.IntegerField(default=0)),
                ('locked', models.BooleanField(default=False)),
                ('status', models.IntegerField(default=0, choices=[(0, b'in review'), (1, b'published'), (2, b'banned')])),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='tools.ToolClassification', null=True)),
            ],
            options={
                'verbose_name_plural': b'Tool Classifications',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tool',
            name='parent',
            field=mptt.fields.TreeForeignKey(to='tools.ToolClassification'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tool',
            name='classifications',
            field=models.ManyToManyField(to='tools.ToolClassification'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UserTool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('callsign', models.CharField(help_text='your nickname for the tool', max_length=255, null=True, blank=True)),
                ('portability', models.IntegerField(default=0, help_text='where the tool can be used', choices=[(0, 'can pickup'), (1, 'dropped off'), (2, 'can use on premisis')])),
                ('owner', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL)),
                ('tool_type', models.ForeignKey(default=None, blank=True, to='tools.Tool')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
