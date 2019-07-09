from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

import json

from pipe.models import Event, Ticket

class PipeViewGETTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create an Event and a Ticket
        Event.objects.create(
            description = json.dumps({'description': "Test Description"}),
            name = "Test Name",
            event_id = 123,
            start_date = timezone.now(),
        )

        event = Event.objects.get(name="Test Name")
        Ticket.objects.create(
            ticket_cost = 1.0,
            event_id = event,
        )

    def test_events_search_list(self):
        """
        Should return json of multiple events with status code 200
        """
        response = self.client.get('/pipe/events/search/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)

    def test_events_search_name(self):
        """
        Should return event with given name and status code 200
        """
        q = "event_name=Test Name"
        response = self.client.get(f"/pipe/events/search/?{q}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)

    def test_events_search_cost(self):
        """
        Should return event with given ticket cost and status code 200
        """
        q = "ticket_cost=1.0"
        response = self.client.get(f"/pipe/events/search/?{q}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)

    def test_events_search_startdate(self):
        """
        Should return event with given start date and status code 200
        """
        tz = timezone.now()
        q = f"start_date={tz.year}-{tz.month}-{tz.day}"
        response = self.client.get(f"/pipe/events/search/?{q}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)

    def test_events_search_error_name(self):
        """
        Should raise 404 if given Event with name does not exist.
        """
        q = "event_name=Not Test Name"
        response = self.client.get(f"/pipe/events/search/?{q}")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.content)

    def test_events_search_error_startdate(self):
        """
        Should raise 404 if given Event with start date does not exist.
        """
        q = f"start_date=2050-01-01"
        response = self.client.get(f"/pipe/events/search/?{q}")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.content)

    def test_events_search_error_cost_dne(self):
        """
        Should raise 404 if given Event with cost does not exist.
        """
        q = f"ticket_cost=-1"
        response = self.client.get(f"/pipe/events/search/?{q}")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.content)

    def test_events_search_error_cost_invalid_input(self):
        """
        Should raise 400 if given invalid input for ticket cost.
        """
        q = f"ticket_cost=hello"
        response = self.client.get(f"/pipe/events/search/?{q}")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.content)



class PipeViewPOSTTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create an Event and a Ticket
        Event.objects.create(
            description = json.dumps({'description': "Test Description"}),
            name = "Test Name",
            event_id = 123,
            start_date = timezone.now(),
        )

        event = Event.objects.get(name="Test Name")
        Ticket.objects.create(
            ticket_cost = 1.0,
            event_id = event,
        )

    def test_events_search_list(self):
        """
        Should return json of multiple events with status code 200
        """
        response = self.client.get('/pipe/events/search/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)
