# Generated by Django 2.2 on 2023-09-03 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app', '0003_auto_20230903_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingmodel',
            name='total_cost',
            field=models.BigIntegerField(default=None),
        ),
    ]