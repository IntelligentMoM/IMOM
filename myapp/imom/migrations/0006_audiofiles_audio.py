# Generated by Django 3.1.6 on 2021-02-18 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imom', '0005_remove_audiofiles_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiofiles',
            name='audio',
            field=models.FileField(default=1, upload_to='upload_audio/'),
            preserve_default=False,
        ),
    ]
