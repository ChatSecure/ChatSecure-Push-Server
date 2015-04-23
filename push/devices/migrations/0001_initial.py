# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('os_type', models.CharField(max_length=255, verbose_name='Operating System Type', choices=[(b'iOS', b'iOS'), (b'Android', b'Android')])),
                ('os_version', models.CharField(max_length=255, null=True, verbose_name='Operating System Version', blank=True)),
                ('device_name', models.CharField(max_length=255, null=True, verbose_name='Device Name', blank=True)),
                ('push_token', models.CharField(max_length=255, verbose_name='Push Token')),
                ('owner', models.ForeignKey(related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
