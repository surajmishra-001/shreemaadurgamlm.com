# Generated by Django 3.2.21 on 2023-10-05 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0005_alter_accociate_bank_ifsc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accociate',
            name='bank_ifsc',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.CreateModel(
            name='Payemt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('status', models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('done', 'done'), ('cancel', 'cancel')], default='pending', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.accociate')),
            ],
        ),
    ]
