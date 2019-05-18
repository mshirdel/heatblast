# Generated by Django 2.2 on 2019-05-06 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('socialnews', '0008_story_url_domain_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='story',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='storycomment',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='socialnews.Story'),
        ),
    ]