# Generated by Django 3.2.5 on 2021-07-30 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_auto_20210315_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(default='/Users/johnmaged/Documents/dev/konaequity/media/profile_photos/generic.png', upload_to='profile_photos/'),
        ),
    ]
