# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('username', models.CharField(max_length=16, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=16)),
                ('following', models.ManyToManyField(to='social.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publicMessage', models.CharField(max_length=4096)),
                ('privateMessage', models.CharField(max_length=4096)),
                ('privateNumber', models.IntegerField(default=0)),
                ('publicNumber', models.IntegerField(default=0)),
                ('text', models.CharField(max_length=4096)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=4096)),
                ('createdby', models.CharField(max_length=16)),
                ('receives', models.CharField(max_length=16)),
                ('mytime', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=4096)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=4096)),
                ('createdby', models.CharField(max_length=16)),
                ('receives', models.CharField(max_length=16)),
                ('mytime', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='privateMessage',
            field=models.ManyToManyField(to='social.PrivateMessage', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='profile',
            field=models.OneToOneField(null=True, to='social.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='publicMessage',
            field=models.ManyToManyField(to='social.PublicMessage', null=True),
            preserve_default=True,
        ),
    ]
