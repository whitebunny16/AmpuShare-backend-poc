# Generated by Django 5.0.3 on 2024-04-22 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_alter_post_image_alter_post_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='video',
        ),
    ]