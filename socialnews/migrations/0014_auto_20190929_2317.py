# Generated by Django 2.2.4 on 2019-09-29 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnews', '0013_socialuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='url',
            new_name='story_url',
        ),
    ]
