# Generated by Django 4.2.16 on 2024-09-17 15:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intake',
            name='date',
        ),
        migrations.AddField(
            model_name='intake',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='intake',
            name='quantity',
            field=models.FloatField(help_text='Quantity in grams or milliliters'),
        ),
    ]
