# Generated by Django 2.2.3 on 2019-07-07 22:46

import django.core.validators
from django.db import migrations, models
import pipe.validators.pipe.events_validators


class Migration(migrations.Migration):

    dependencies = [
        ('pipe', '0003_auto_20190707_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.IntegerField(validators=[pipe.validators.pipe.events_validators.validate_id, django.core.validators.MinValueValidator(0)]),
        ),
    ]
