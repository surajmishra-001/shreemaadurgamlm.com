# Generated by Django 3.2.21 on 2023-09-29 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0004_auto_20230929_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accociate',
            name='bank_ifsc',
            field=models.CharField(default='Bank Ifsc Code..', max_length=150),
        ),
    ]
