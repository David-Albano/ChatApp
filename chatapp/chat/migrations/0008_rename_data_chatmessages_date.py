# Generated by Django 4.1.5 on 2023-02-01 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_chatmessages_id_conversation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatmessages',
            old_name='data',
            new_name='date',
        ),
    ]
