# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('name', models.CharField(help_text='The name of the hub', max_length=200)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=200, blank=True, unique=True)),
                ('is_enabled', models.BooleanField(default=True)),
                ('is_private', models.BooleanField(default=False)),
            ],
            options={
                'ordering': [b'name'],
                'verbose_name': 'hub',
                'verbose_name_plural': 'hubs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HubOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('hub', models.OneToOneField(to='hubs.Hub')),
            ],
            options={
                'verbose_name': 'hub owner',
                'verbose_name_plural': 'hub owners',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HubUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'ordering': [b'hub', b'user'],
                'verbose_name': 'hub user',
                'verbose_name_plural': 'hub users',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hubowner',
            name='hub_user',
            field=models.OneToOneField(to='hubs.HubUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hub',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='hubs.HubUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hubuser',
            name='hub',
            field=models.ForeignKey(to='hubs.Hub'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hubuser',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='hubuser',
            unique_together=set([(b'user', b'hub')]),
        ),
    ]
