# Generated by Django 3.2.15 on 2023-09-22 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0008_auto_20230922_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(verbose_name='комментарий'),
        ),
    ]
