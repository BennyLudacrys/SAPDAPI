# Generated by Django 4.2.2 on 2023-09-06 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_post_block_post_housenumber_post_neighborhood'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date_of_disappearance',
            field=models.CharField(max_length=255, null=True),
        ),
    ]