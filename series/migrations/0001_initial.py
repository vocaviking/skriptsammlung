# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(help_text='Enter a meaningful name, to make this file easier to find.', max_length=50, default='')),
                ('lecture', models.CharField(help_text='Enter the lecture which this file belongs to.', verbose_name='Lecture', max_length=50, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('file', models.FileField(help_text='Only PDF, TXT, TEX and JPG files under ? MB.', verbose_name='File Selection', upload_to='series')),
                ('date', models.DateTimeField(verbose_name='Upload Date', default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(editable=False, primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('title', models.CharField(help_text='e.g. Dr., Prof., Sir', blank=True, max_length=20, verbose_name='Title', default='')),
                ('about_me', models.TextField(help_text='Tell other Users who you are, and what you do.', blank=True, verbose_name='About Me', default='')),
                ('image', models.ImageField(help_text='TODO', blank=True, upload_to='user_images', verbose_name='Profile Image', null=True)),
                ('website', models.URLField(help_text='TODO', blank=True, verbose_name='Personal Website', default='')),
                ('phone', models.CharField(help_text='TODO', blank=True, max_length=20, verbose_name='Phone Number', default='')),
                ('birth_date', models.DateField(help_text='Your Birthdate will only be shown to other Users with your permission.', verbose_name='Birthdate', default=django.utils.timezone.now)),
                ('show_email', models.BooleanField(help_text='Show other Users your Mail Address.', verbose_name='Show Mail Adress', default=False)),
                ('show_age', models.BooleanField(help_text='Show other Users how old you are.', verbose_name='Show Age', default=False)),
                ('show_birthday', models.BooleanField(help_text='Show other Users the Day and Month of your Birthday.', verbose_name='Show Birthday', default=False)),
                ('show_realname', models.BooleanField(help_text='Show other Users your First and Last Name.', verbose_name='Show Realname', default=False)),
                ('last_ip', models.GenericIPAddressField(help_text='TODO', verbose_name='Last known IP-address of the User', default='0.0.0.0', editable=False)),
            ],
        ),
        migrations.AddField(
            model_name='upload',
            name='uploader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Uploader'),
        ),
        migrations.AddField(
            model_name='meta',
            name='upload',
            field=models.ManyToManyField(to='series.Upload', blank=True),
        ),
    ]
