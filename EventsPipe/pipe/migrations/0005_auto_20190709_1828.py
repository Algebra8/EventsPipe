# Generated by Django 2.2.3 on 2019-07-09 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipe', '0004_auto_20190707_2246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='event_id',
            new_name='event',
        ),
    ]