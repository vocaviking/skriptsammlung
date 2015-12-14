# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0010_upload_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(null=True, blank=True, upload_to='user_images', verbose_name='Profile Image'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_ip',
            field=models.GenericIPAddressField(verbose_name='Last known IP-address of the User', editable=False, default='0.0.0.0'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Phone Number', default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='website',
            field=models.URLField(blank=True, verbose_name='Personal Website', default=''),
        ),
    ]
