# Generated by Django 4.2.2 on 2023-08-30 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_user_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, upload_to='person_pictures'),
        ),
    ]
