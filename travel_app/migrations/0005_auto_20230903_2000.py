# Generated by Django 2.2 on 2023-09-03 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app', '0004_auto_20230903_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingmodel',
            name='total_cost',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]
