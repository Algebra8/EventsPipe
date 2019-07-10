from django.db import models
from django.utils import timezone
from .validators.pipe import events_validators
from .validators.pipe import tickets_validators
from django.core.validators import MinValueValidator

class Event(models.Model):
    description = models.TextField(blank=False)
    name = models.CharField(
        max_length=550,
        blank=False,
    )
    event_id = models.IntegerField(
        validators=[
            events_validators.validate_id,
            MinValueValidator(0),
        ],
        blank=False,
    )
    start_date = models.DateTimeField(
        'start date',
        default=timezone.now,
        validators=[events_validators.validate_startdate],
        blank=False,
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Event'


class Ticket(models.Model):
    ticket_cost = models.FloatField(
        blank=False,
        validators=[tickets_validators.validate_cost,]
    )
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        blank=False,
    )

    def __str__(self):
        return str(self.ticket_cost)

    def __repr__(self):
        return 'Ticket'
