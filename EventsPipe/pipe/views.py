# Django tools
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils.decorators import decorator_from_middleware
# Middleware and validators
from .middleware.pipe.request_middleware import HeaderValidation
from .validators.pipe.views_validators import request_validation
import json
# Models
from pipe.models import Event, Ticket


def index(request):
    html = "<h1>goobye wordle</h1>"
    return HttpResponse(html)


@decorator_from_middleware(HeaderValidation)
def get_event_by_name(request, event_name):
    ev = Event.objects.get(name=event_name)
    data = json.loads(ev.description)

    return JsonResponse(data)


@decorator_from_middleware(HeaderValidation)
def get_event_by_id(request, eventid):
    ev = Event.objects.get(event_id=int(eventid))
    data = json.loads(ev.description)

    return JsonResponse(data)


@decorator_from_middleware(HeaderValidation)
def get_events_by_cost(request, cost):
    events_dict = dict()
    # Tickets contain one or more events
    tickets = Ticket.objects.filter(ticket_cost=float(cost))
    events = [json.loads(t.event_id.description) for t in tickets]
    # For multiple JSON responses, assign all required events to dict
    N_events = len(tickets)  # number of events for given ticket cost
    for i in range(N_events):
        if i not in events_dict:
            events_dict[i] = events[i]

    return JsonResponse(events_dict)


@decorator_from_middleware(HeaderValidation)
def get_by_startdate(request, utc_startdate):
    event_dict = {}
    parsed_sd = parse_datetime(utc_startdate)
    """
    `event` is a list containing all the different events for
    any single start date.
    """
    events_by_sd = Event.objects.filter(start_date=parsed_sd)
    events = [json.loads(e.description) for e in events_by_sd]
    N_events = len(events)
    for i in range(N_events):
        if i not in event_dict:
            event_dict[i] = events[i]
        else:
            # Unique indices, won't get here
            pass

    return JsonResponse(event_dict)


@csrf_exempt
@decorator_from_middleware(HeaderValidation)
def update_event(request, eventid):
    if request.method == 'POST':
        # Get Event and convert JSON description to python dict
        event = Event.objects.get(event_id=eventid)
        event_dict = json.loads(event.description)

        # Go through request and update event
        if request.body:
            body = json.loads(request.body)

            # Check if JSON request is valid
            not_valid = request_validation(body, event_dict)
            if not_valid:
                return not_valid

            # Update Event JSON
            for key, val in body.items():
                event_dict[key] = val

        # Update fields of Event object
        event.name = event_dict['name']
        event.event_id = event_dict['id']
        event.start_date = parse_datetime(event_dict['start']['utc'])

        # Convert object back to JSON and place in event
        event.description = json.dumps(event_dict)

        # Validate request before saving
        try:
            event.full_clean()
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)

        # Note django will automatically update
        # the object if pk is an existing value
        event.save()

        return JsonResponse(json.loads(event.description))


    msg = 'This endpoint is used for POST request and only accepts ' \
        + 'JSON objects. If you are seeing then you either did not make a ' \
        + 'POST request or forgot to send the POST in the body of the ' \
        + 'request as a JSON object.'

    return JsonResponse({
        'Error': "I'm a teapot",
        'message': msg,
    }, status=418)
