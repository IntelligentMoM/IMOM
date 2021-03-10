# Generated by Django 3.1.6 on 2021-02-18 06:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('imom', '0003_remove_audiofiles_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiofiles',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]