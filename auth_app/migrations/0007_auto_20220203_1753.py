# Generated by Django 3.2.5 on 2022-02-03 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0006_auto_20211201_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='customer_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(default='/mnt/e/AliAsghar/Django/Django/konaequity/konaequity/media/profile_photos/generic.png', upload_to='profile_photos/'),
        ),
    ]
