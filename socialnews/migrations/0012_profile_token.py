# Generated by Django 2.2.3 on 2019-08-04 11:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('socialnews', '0011_auto_20190724_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='token',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
