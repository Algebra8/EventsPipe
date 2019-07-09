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
            description = json.dumps({'description': "Test Description 1"}),
            name = "Test Name 1",
            event_id = 123,
            start_date = timezone.now(),
        )

        Event.objects.create(
            description = json.dumps({'description': "Test Description 2"}),
            name = "Test Name 2",
            event_id = 321,
            start_date = timezone.now(),
        )

        event = Event.objects.get(name="Test Name 1")
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
        # Convert to dict to get number of elements of json
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_events_search_name(self):
        """
        Should return event with given name and status code 200
        """
        q = "event_name=Test Name 1"
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
            description = json.dumps({
                'name': 'Test Description',
                'id': 123,
                'start': {'utc': str(timezone.now())},
            }),
            name = "Test Name",
            event_id = 123,
            start_date = timezone.now(),
        )

        event = Event.objects.get(name="Test Name")
        Ticket.objects.create(
            ticket_cost = 1.0,
            event_id = event,
        )


    def test_events_update_url(self):
        """
        Should return json of updated event with status code 200
        """
        headers={'HTTP_X_AUTH': 'GENERIC_AUTH_KEY'}
        response = self.client.post(
            '/pipe/events/update/123',
            content_type='application/json',
            data={
                "name": "abc",
                "start": {"utc": str(timezone.now())},
                "id": 321,
            },
            **headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)

    def test_events_update_bad_input(self):
        """
        Should return 400 when given bad input
        """
        headers={'HTTP_X_AUTH': 'GENERIC_AUTH_KEY'}
        response = self.client.post(
            '/pipe/events/update/123',
            content_type='application/json',
            data={'blah': 123},
            **headers,
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.content)

    def test_events_update_no_input(self):
        """
        Should return 418 when given no json request
        """
        headers={'HTTP_X_AUTH': 'GENERIC_AUTH_KEY'}
        response = self.client.post(
            '/pipe/events/update/123',
            content_type='application/json',
            data={},
            **headers,
        )
        self.assertEqual(response.status_code, 418)
        self.assertTrue(response.content)

    def test_events_update_event_DNE(self):
        """
        Should return 404 when Event DNE
        """
        headers={'HTTP_X_AUTH': 'GENERIC_AUTH_KEY'}
        response = self.client.post(
            '/pipe/events/update/0',
            content_type='application/json',
            data={},
            **headers,
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.content)

    def test_events_update_wrong_auth(self):
        """
        Should return 401 if headers set to wrong
        value
        """
        headers={'HTTP_X_AUTH': 'WRONG HEADER VALUE'}
        response = self.client.post(
            '/pipe/events/update/0',
            content_type='application/json',
            data={'name': 'new name'},
            **headers,
        )
        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.content)

    def test_events_update_no_auth(self):
        """
        Should return 401 if headers not set
        """
        response = self.client.post(
            '/pipe/events/update/0',
            content_type='application/json',
            data={'name': 'new name'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.content)
