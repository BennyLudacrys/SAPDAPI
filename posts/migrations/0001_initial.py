# Generated by Django 4.2.2 on 2023-07-31 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('nationality', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('date_of_birth', models.CharField(max_length=255, null=True)),
                ('last_seen_location', models.CharField(blank=True, max_length=255)),
                ('cellphone', models.CharField(blank=True, max_length=255)),
                ('cellphone1', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField()),
                ('disease', models.CharField(blank=True, max_length=255)),
                ('picture', models.ImageField(upload_to='person_pictures')),
                ('status', models.CharField(blank=True, max_length=255)),
                ('desc', models.TextField(blank=True)),
                ('is_complete', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
