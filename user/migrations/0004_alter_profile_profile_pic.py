# Generated by Django 5.0.2 on 2024-03-01 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_profile_first_name_remove_profile_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
