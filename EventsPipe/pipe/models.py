from django.db import models

class Event(models.Model):
    description = models.TextField()
    name = models.CharField(max_length=550)
    event_id = models.IntegerField()
    start_date = models.DateTimeField('start date')

    def __str__(self):
        return self.name

class Ticket(models.Model):
    ticket_cost = models.FloatField()
    event_id = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.ticket_cost)
