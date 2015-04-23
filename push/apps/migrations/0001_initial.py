# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PushApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sandbox_mode', models.BooleanField(verbose_name=b'Sandbox Mode')),
                ('apns_cert', models.TextField(null=True, verbose_name=b'APNS Certificate', blank=True)),
                ('gcm_api_key', models.TextField(null=True, verbose_name=b'Google Cloud Messaging API Key', blank=True)),
                ('itunes_shared_secret', models.CharField(max_length=50, null=True, verbose_name=b'iTunes Shared Secret', blank=True)),
            ],
        ),
    ]
