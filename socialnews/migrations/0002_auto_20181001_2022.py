# Generated by Django 2.1.1 on 2018-10-01 20:22

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='modified',
            field=django_jalali.db.models.jDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='itemcomment',
            name='created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='itemcomment',
            name='modified',
            field=django_jalali.db.models.jDateTimeField(auto_now=True),
        ),
    ]
