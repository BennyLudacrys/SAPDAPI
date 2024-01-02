# Generated by Django 4.2.2 on 2023-12-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
        ('posts', '0010_post_latitude_post_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments_post', to='comments.comment'),
        ),
    ]