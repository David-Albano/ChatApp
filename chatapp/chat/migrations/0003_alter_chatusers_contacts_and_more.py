# Generated by Django 4.1.5 on 2023-01-30 22:09

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_conversations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatusers',
            name='contacts',
            field=models.CharField(max_length=10000000),
        ),
        migrations.AlterField(
            model_name='conversations',
            name='id_serial',
            field=models.CharField(default=chat.models.create_id_serial, max_length=61, unique=True),
        ),
    ]
