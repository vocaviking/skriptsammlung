# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0015_auto_20160119_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_ip',
        ),
    ]
