# Generated by Django 2.1.1 on 2018-10-09 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialnews', '0002_auto_20181001_2022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('modified', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=500)),
                ('url', models.URLField(blank=True, max_length=2000, null=True)),
                ('story_body_text', models.TextField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoryComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('modified', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('story_comment', models.TextField()),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='socialnews.StoryComment')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialnews.Story')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='item',
            name='user',
        ),
        migrations.RemoveField(
            model_name='itemcomment',
            name='commenter',
        ),
        migrations.RemoveField(
            model_name='itemcomment',
            name='item',
        ),
        migrations.RemoveField(
            model_name='itemcomment',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='ItemComment',
        ),
    ]
