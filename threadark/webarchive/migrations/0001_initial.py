# Generated by Django 5.1.6 on 2025-02-27 06:53

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5, unique=True)),
                ('long_name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('thread_id', models.BigIntegerField()),
                ('board', models.CharField(max_length=5)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(default='open', max_length=15)),
                ('url', models.URLField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('replies', models.IntegerField(default=0)),
                ('response_json', models.JSONField(blank=True, null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['board', 'thread_id'], name='webarchive__board_329460_idx')],
                'unique_together': {('board', 'thread_id')},
            },
        ),
        migrations.CreateModel(
            name='TwoFactorCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('board', models.CharField(max_length=5)),
                ('message_id', models.CharField(max_length=50)),
                ('text', models.TextField(blank=True, null=True)),
                ('time', models.DateTimeField()),
                ('has_audio', models.BooleanField(default=False)),
                ('image_url', models.URLField(blank=True, max_length=255, null=True)),
                ('audio_url', models.URLField(blank=True, max_length=255, null=True)),
                ('thread_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webarchive.thread')),
            ],
            options={
                'indexes': [models.Index(fields=['board', 'thread_id', 'message_id'], name='webarchive__board_18b419_idx')],
                'unique_together': {('board', 'thread_id', 'message_id')},
            },
        ),
    ]
