# Generated by Django 2.2 on 2023-09-04 15:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel_app', '0012_commentmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='commentModel',
            new_name='reviewModel',
        ),
    ]
