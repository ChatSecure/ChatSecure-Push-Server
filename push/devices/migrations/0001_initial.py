# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='APNSDevice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name', blank=True)),
                ('active', models.BooleanField(default=True, help_text='Inactive devices will not be sent notifications', verbose_name='Is active')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date', null=True)),
                ('registration_id', models.TextField(verbose_name='Registration ID')),
                ('device_id', models.TextField(null=True, verbose_name='Device ID', blank=True)),
                ('owner', models.ForeignKey(related_name='apns_devices', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,)),
            ],
            options={
                'verbose_name': 'APNS device',
            },
        ),
        migrations.CreateModel(
            name='GCMDevice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name', blank=True)),
                ('active', models.BooleanField(default=True, help_text='Inactive devices will not be sent notifications', verbose_name='Is active')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date', null=True)),
                ('registration_id', models.TextField(verbose_name='Registration ID')),
                ('device_id', models.TextField(null=True, verbose_name='Device ID', blank=True)),
                ('owner', models.ForeignKey(related_name='gcm_devices', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,)),
            ],
            options={
                'verbose_name': 'GCM device',
            },
        ),
    ]
