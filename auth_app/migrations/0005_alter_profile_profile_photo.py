# Generated by Django 3.2.5 on 2021-08-15 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_alter_profile_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(default='/home/Konaequity/konaequity/media/profile_photos/generic.png', upload_to='profile_photos/'),
        ),
    ]
