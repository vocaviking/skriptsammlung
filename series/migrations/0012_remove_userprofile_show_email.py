# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0011_auto_20151214_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='show_email',
        ),
    ]
