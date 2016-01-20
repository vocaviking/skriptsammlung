# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0012_remove_userprofile_show_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='degree',
            field=models.CharField(blank=True, default='', verbose_name='Degree', help_text='e.g. PhD, B.Sc., M.Sc.', max_length=50),
        ),
    ]
