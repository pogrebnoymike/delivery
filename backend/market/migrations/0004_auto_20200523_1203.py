# Generated by Django 3.0.5 on 2020-05-23 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_auto_20200523_1024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]
