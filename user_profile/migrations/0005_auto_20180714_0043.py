# Generated by Django 2.0.3 on 2018-07-14 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_auto_20180713_2335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='_is_admin',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='_is_hacker',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='_is_mentor',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='_is_staff',
        ),
        migrations.AddField(
            model_name='profile',
            name='_update_field',
            field=models.BooleanField(default=False),
        ),
    ]
