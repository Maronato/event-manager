# Generated by Django 2.1.7 on 2019-03-24 03:32

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_squashed_0006_auto_20190320_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='require_payment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='settings',
            name='ticket_price',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01000000000000000020816681711721685132943093776702880859375'))]),
        ),
    ]