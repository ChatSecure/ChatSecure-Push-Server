# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('token', models.CharField(unique=True, max_length=100, verbose_name=b'Whitelist Token')),
                ('apns_device', models.ForeignKey(blank=True, to='devices.APNSDevice', null=True, on_delete=models.CASCADE,)),
                ('gcm_device', models.ForeignKey(blank=True, to='devices.GCMDevice', null=True, on_delete=models.CASCADE,)),
                ('owner', models.ForeignKey(related_name='tokens', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)),
            ],
        ),
    ]
