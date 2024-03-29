# Generated by Django 2.2.3 on 2019-07-10 07:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pipe.validators.pipe.events_validators
import pipe.validators.pipe.tickets_validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('name', models.CharField(max_length=550)),
                ('event_id', models.BigIntegerField(validators=[pipe.validators.pipe.events_validators.validate_id])),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, validators=[pipe.validators.pipe.events_validators.validate_startdate], verbose_name='start date')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_cost', models.FloatField(validators=[pipe.validators.pipe.tickets_validators.validate_cost])),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pipe.Event')),
            ],
        ),
    ]
