# Generated by Django 2.2.4 on 2020-01-10 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_posts_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_images'),
        ),
    ]
