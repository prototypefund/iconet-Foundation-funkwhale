# Generated by Django 3.2.4 on 2021-07-03 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0003_auto_20171214_2205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ['domain'], 'verbose_name': 'site', 'verbose_name_plural': 'sites'},
        ),
    ]