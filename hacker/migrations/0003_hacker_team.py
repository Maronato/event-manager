# Generated by Django 2.1.7 on 2019-03-24 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
        ('hacker', '0002_auto_20190320_0034_squashed_0004_auto_20190321_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='hacker',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hackers', to='team.Team'),
        ),
    ]