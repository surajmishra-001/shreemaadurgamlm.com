# Generated by Django 3.2.21 on 2023-10-31 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0010_agent_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='is_active',
        ),
        migrations.AddField(
            model_name='accociate',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
