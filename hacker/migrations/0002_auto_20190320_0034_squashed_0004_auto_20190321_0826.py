# Generated by Django 2.1.7 on 2019-03-23 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('hacker', '0002_auto_20190320_0034'), ('hacker', '0003_auto_20190320_1119'), ('hacker', '0004_auto_20190321_0826')]

    dependencies = [
        ('hacker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hacker',
            name='transaction_reference',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
    ]
