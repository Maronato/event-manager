# Generated by Django 2.1.7 on 2019-03-24 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_squashed_0010_shortcuts_is_mentor'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortcuts',
            name='payment_state',
            field=models.CharField(default='', max_length=20),
        ),
    ]
