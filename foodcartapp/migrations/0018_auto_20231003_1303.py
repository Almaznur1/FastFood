# Generated by Django 3.2.15 on 2023-10-03 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0017_auto_20231002_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='order',
            name='lon',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='lon',
        ),
    ]
