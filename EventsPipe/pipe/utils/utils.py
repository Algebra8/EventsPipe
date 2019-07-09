import django
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventsPipe.settings')
django.setup()

# Django tools
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils import timezone
import json
import datetime
# Models
from pipe.models import Event, Ticket


def convert_string_to_timezone(date):
    """
    Function to convert a string datetime format
    to a timezone aware datetime.datetime object
    """
    # Convert string to datetime based on %Y-%m-%d
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    # Convert and return datetime to datetime with timezone
    return timezone.make_aware(date)


def events_list_to_dict(N_events, events_list):
    """
    Function to conver a list of events to a JSON
    object, where keys 0-N_events are JSON events
    """
    events_dict = dict()
    for i in range(N_events):
        if i not in events_dict:
            events_dict[i] = events_list[i]
        else:
            # Unique indices, won't get here
            pass

    return events_dict


def get_events_list():
    """
    Controller helper function to return
    JSON list of events or 404

    returns: JSON list of events or 404
    url: pipe/events/search/
    """
    try:
        events_dict = dict()
        events = Event.objects.all()

    except Event.DoesNotExist:
        err = "Could not access Event records."
        return JsonResponse({'error': err}, status=404)

    else:
        # Get descriptions of events
        event_descr = [json.loads(e.description) for e in events]
        # Convert list of events to dictionary
        N_events = len(event_descr)
        events_dict = events_list_to_dict(N_events, event_descr)

        return JsonResponse(events_dict)


def get_event_by_name(event_name):
    """
    Controller helper function to return event with
    given name (event_name) or 404

    returns: JSON event or 404
    url: pipe/events/search/?event_name=...
    """
    try:
        ev = Event.objects.get(name=event_name)

    except Event.DoesNotExist:
        return JsonResponse({
            'event name': event_name,
            'error': 'The given Event does not exist.'
        }, status=404)

    else:
        data = json.loads(ev.description)
        return JsonResponse(data)


def get_event_by_id(eventid):
    """
    Controller helper function to return event with
    given id (eventid) or 404

    returns: JSON event or 404
    """
    try:
        ev = Event.objects.get(event_id=int(eventid))

    except Event.DoesNotExist:
        return JsonResponse({
            'event id': eventid,
            'error': 'The given Event does not exist.'
        }, status=404)

    else:
        data = json.loads(ev.description)
        return JsonResponse(data)


def get_events_by_cost(cost):
    """
    Controller helper function to return event with
    given ticket cost (cost) or 404

    returns: JSON list of events or 404
    url: pipe/events/search/?ticket_cost=...
    """
    try:
        # Tickets contain one or more events
        # For issues with `filter`, refer to get_by_startdate
        tickets = Ticket.objects.filter(ticket_cost=float(cost))

    except Ticket.DoesNotExist:
        return JsonResponse({
            'ticket cost': cost,
            'error': f"The given Event with cost {cost} does not exist."
        }, status=404)

    except ValueError:
        return JsonResponse({
            'ticket cost': cost,
            'error': "Ticket cost must be float or integer values."
        }, status=400)

    else:
        if not tickets:
            # Return 404 for consistency within API
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
            return JsonResponse({
                'ticket cost': cost,
                'error': 'No events match for the given ticket cost.'
            }, status=404)

        events = [json.loads(t.event.description) for t in tickets]
        # For multiple JSON responses, assign all required events to dict
        N_events = len(tickets)  # number of events for given ticket cost
        events_dict = events_list_to_dict(N_events, events)

        return JsonResponse(events_dict)


def get_by_startdate(utc_startdate):
    """
    Controller helper function to return event with
    given ticket cost (cost) or 404

    returns: JSON list of events or 404
    url: pipe/events/search/?start_date=...
    """
    try:
        # utc_startdate must be in format %Y-%m-%d
        parsed_sd = convert_string_to_timezone(utc_startdate)

        # `filter` is used instead of `get` since multiple
        # events can be on a given day.
        # Note `filter` does not raise 404 if not found,
        # queryset will be empty.
        events_by_sd = Event.objects.filter(
            start_date__year=parsed_sd.year,
            start_date__month=parsed_sd.month,
            start_date__day=parsed_sd.day,
        )

    except Event.DoesNotExist:
        # Proper date given, Event does not exist
        # This will not happen with `filter`
        return JsonResponse({
            'event start date': utc_startdate,
            'error': 'The given Event does not exist.'
        }, status=404)

    except ValueError:
        # Improper date format given
        return JsonResponse({
            'event start date': utc_startdate,
            'error': 'Bad Request',
            'Message': "Format must be 'YYYY-MM-DD'."
        }, status=400)

    else:
        if not events_by_sd:
            # Return 404 for consistency within API
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
            return JsonResponse({
                'event start date': utc_startdate,
                'error': 'No events match the given date.'
            }, status=404)

        # `event` is a list containing all the different events for
        # any single start date.
        events = [json.loads(e.description) for e in events_by_sd]

        # Convert event descriptions to python dict
        N_events = len(events)
        events_dict = events_list_to_dict(N_events, events)

        return JsonResponse(events_dict)
