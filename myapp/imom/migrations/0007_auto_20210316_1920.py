# Generated by Django 3.1.6 on 2021-03-16 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imom', '0006_audiofiles_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofiles',
            name='audio',
            field=models.FileField(upload_to='media/<django.db.models.fields.related.ForeignKey>'),
        ),
    ]
