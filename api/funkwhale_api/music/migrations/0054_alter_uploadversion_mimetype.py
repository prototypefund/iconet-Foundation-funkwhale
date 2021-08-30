# Generated by Django 3.2.4 on 2021-07-03 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0053_denormalize_audio_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadversion',
            name='mimetype',
            field=models.CharField(choices=[('audio/mp3', 'mp3'), ('audio/mpeg3', 'mp3'), ('audio/x-mp3', 'mp3'), ('audio/mpeg', 'mp3'), ('video/ogg', 'ogg'), ('audio/ogg', 'ogg'), ('audio/opus', 'opus'), ('audio/x-m4a', 'aac'), ('audio/x-m4a', 'm4a'), ('audio/x-flac', 'flac'), ('audio/flac', 'flac'), ('audio/aiff', 'aif'), ('audio/x-aiff', 'aif'), ('audio/aiff', 'aiff'), ('audio/x-aiff', 'aiff')], max_length=50),
        ),
    ]