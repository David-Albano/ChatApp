# Generated by Django 4.1.5 on 2023-02-02 21:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_alter_chatmessages_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessages',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
