# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LendingAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('action', models.IntegerField(default=0, choices=[(0, b'requested'), (1, b'lent'), (2, b'received'), (3, b'returned'), (4, b'lost'), (5, b'returned-damaged')])),
            ],
            options={
                'ordering': (b'created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('purpose', models.TextField()),
                ('hub', models.ForeignKey(default=None, to='hubs.Hub')),
            ],
            options={
                'ordering': (b'created',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lendingaction',
            name='transaction',
            field=models.ForeignKey(to='lending.Transaction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='last_action',
            field=models.ForeignKey(blank=True, to='lending.LendingAction', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='lendee',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='tool',
            field=models.ForeignKey(default=None, to='tools.UserTool'),
            preserve_default=True,
        ),
    ]
