# Generated by Django 2.2 on 2023-09-01 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='regionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(default=None, upload_to='regions')),
            ],
        ),
        migrations.CreateModel(
            name='userModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('phone', models.PositiveIntegerField()),
                ('image', models.ImageField(blank=True, default=None, upload_to='users')),
            ],
        ),
        migrations.CreateModel(
            name='planModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(default=None, upload_to='plans')),
                ('detail', models.TextField()),
                ('price_for_adult_per_day', models.IntegerField(default=15000)),
                ('price_for_child_per_day', models.IntegerField(default=10000)),
                ('region', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='travel_app.regionModel')),
            ],
        ),
    ]
