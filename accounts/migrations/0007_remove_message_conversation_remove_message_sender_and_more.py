# Generated by Django 5.1 on 2024-08-17 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_conversation_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
