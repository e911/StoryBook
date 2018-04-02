# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-19 07:49
from __future__ import unicode_literals

import account.models
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('photo', models.ImageField(blank=True, height_field='height', null=True, upload_to=account.models.upload_location, width_field='width')),
                ('height', models.IntegerField(default=0)),
                ('width', models.IntegerField(default=0)),
                ('bio', models.TextField(blank=True, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('gender', models.PositiveIntegerField(choices=[(0, 'Not Known'), (1, 'Male'), (2, 'Female'), (9, 'Others')], default=0)),
                ('follower', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), blank=True, null=True, size=None)),
                ('following', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), blank=True, null=True, size=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('content', models.TextField(blank=True, null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Receiver', to='account.Author')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Sender', to='account.Author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('seen', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Author')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
