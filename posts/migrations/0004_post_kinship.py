# Generated by Django 4.2.2 on 2023-08-12 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_post_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='kinship',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]