from django.test import TestCase
from pipe.models import Event, Ticket
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime


class EventModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Event.objects.create(
            description = "Test Description",
            name = "Test Name",
            event_id = "123",
            start_date = timezone.now(),
        )

    def test_event_exists(self):
        """
        Should return True if object exists
        """
        event = Event.objects.get(name="Test Name")
        self.assertTrue(event)

    def test_invalid_event_id_type(self):
        """
        Should raise ValidationError if wrong
        type is put for `event_id`

        tests: event_validators.validate_id
        """
        event = Event.objects.get(name="Test Name")
        with self.assertRaises(ValidationError):
            event.event_id = "not an int id"
            event.full_clean()

    def test_invalid_event_id_value(self):
        """
        Should raise ValidationError if `event_id`
        value is less than 0

        tests: django.core.validators.MinValueValidator(0)
        """
        event = Event.objects.get(name="Test Name")
        with self.assertRaises(ValidationError):
            event.event_id = -1
            event.full_clean()

    def test_valid_event_id(self):
        """
        Should change `event_id` to 5

        tests: models.CharField
        """
        event = Event.objects.get(name="Test Name")

        try:
            event.event_id = 5
            self.assertEqual(event.event_id, 5)
        except ValidationError:
            self.fail("Exception raised unexpectedly.")

    def test_invalid_name(self):
        """
        Should raise ValidationError if length
        of `name` is greater than 550 characters

        tests: models.max_length
        """
        event = Event.objects.get(name="Test Name")
        new_name = "a"*1000
        with self.assertRaises(ValidationError):
            event.name = new_name
            event.full_clean()

    def test_valid_name(self):
        """
        Should change `name` to new_name

        tests: models.IntegerField
        """
        event = Event.objects.get(name="Test Name")
        new_name = "Hawaii Bar Lounge"

        try:
            event.name = new_name
            event.full_clean()
            self.assertEqual(event.name, new_name)
        except ValidationError:
            self.fail("Exception raised unexpectedly.")

    def test_invalid_start_date(self):
        """
        Should raise ValidationError if length
        of `name` is greater than 550 characters

        tests: events_validators.validate_startdate
        """
        event = Event.objects.get(name="Test Name")
        new_start_date = "hello"
        with self.assertRaises(ValidationError):
            event.start_date = new_start_date
            event.full_clean()

    def test_valid_start_date(self):
        """
        Should change `start_date` to new_start_date

        tests: models.DateTimeField
        """
        event = Event.objects.get(name="Test Name")
        new_start_date = "1995-08-12"
        try:
            event.start_date = new_start_date
            event.full_clean()
            # Full clean converts string to datetime
            # Convert datetime to timezone aware datetime
            event.start_date = timezone.make_aware(event.start_date)
            self.assertTrue(event.start_date.tzinfo)
        except ValidationError:
            self.fail("Exception raised unexpectedly.")


class TicketModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Ticket.objects.create(
            ticket_cost = 1.0,

            event_id = Event.objects.create(
                description = "Test Description",
                name = "Test Name",
                event_id = "123",
                start_date = timezone.now(),
            )
        )

    def test_ticket_exists(self):
        """
        Should return True if object exists
        """
        ticket = Ticket.objects.get(ticket_cost=1.0)
        self.assertTrue(ticket)

    def test_invalid_ticket_cost(self):
        """
        Should raise ValidationError if wrong
        type is put for `ticket_cost`

        Note, not necessary to check for type
        int since model will automatically convert
        int to float

        tests: ticket_validators.validate_cost
        """
        ticket = Ticket.objects.get(ticket_cost=1.0)
        with self.assertRaises(ValidationError):
            ticket.ticket_cost = "not a float"
            ticket.full_clean()


    def test_invalid_ticket_event(self):
        """
        Should raise ValueError if `event_id` is
        not set as an Event

        tests: models.ForeignKey
        """
        ticket = Ticket.objects.get(ticket_cost=1.0)
        with self.assertRaises(ValueError):
            ticket.event_id = 10
            ticket.full_clean()

    def test_valid_ticket_cost_0(self):
        """
        Should set `ticket_cost` to 5.0 when given
        5 as an int

        tests: models.FloatField
        """
        ticket = Ticket.objects.get(ticket_cost=1.0)

        try:
            ticket.ticket_cost = 5
            self.assertEqual(ticket.ticket_cost, 5.0)
        except ValidationError:
            self.fail("Exception raised unexpectedly.")

    def test_valid_ticket_cost_1(self):
        """
        Should set `ticket_cost` to 5.0 when tiven
        5 as a float

        tests: models.FloatField
        """
        ticket = Ticket.objects.get(ticket_cost=1.0)

        try:
            ticket.ticket_cost = 5.0
            self.assertEqual(ticket.ticket_cost, 5.0)
        except ValidationError:
            self.fail("Exception raised unexpectedly.")
