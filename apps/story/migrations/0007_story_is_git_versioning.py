# Generated by Django 3.1 on 2022-12-14 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0006_auto_20221213_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='is_git_versioning',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
