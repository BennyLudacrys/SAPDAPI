# Generated by Django 4.2.2 on 2023-08-04 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='desc',
        ),
    ]
