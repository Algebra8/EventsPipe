# Django tools
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils.decorators import decorator_from_middleware
from django.utils import timezone
# Middleware and validators
from .middleware.pipe.request_middleware import HeaderValidation
from .validators.pipe.views_validators import request_validation
import json
import datetime
# Models
from pipe.models import Event, Ticket
# Utils
from pipe.utils import utils


def index(request):
    # Tired of Hello Worlds...
    html = "<h1>goobye wordle</h1>"
    return HttpResponse(html)

def get_event(request):
    """
    Endpoint for querying Events
    """
    if request.method == 'GET':
        q = request.GET.dict()
        err_msg = "Please query by only event_name, start_date, ticket_cost " \
            + "or none for a list of events."

        if not q:
            # Return JSON of list of all Events
            return utils.get_events_list()

        if len(q) > 1:
            return JsonResponse({'error': err_msg}, status=400)

        try:
            if 'event_name' in q:
                return utils.get_event_by_name(q['event_name'])
            elif 'start_date' in q:
                return utils.get_by_startdate(q['start_date'])
            elif 'ticket_cost' in q:
                return utils.get_events_by_cost(q['ticket_cost'])

        except KeyError:
            return JsonResponse({'error': err_msg}, status=400)

    return JsonResponse({
        'error': 'This endpoint is for GET requests only'
    }, status=404)


@csrf_exempt
@decorator_from_middleware(HeaderValidation)
def update_event(request, eventid):
    """
    Endpoint for POST request to update an existing Event
    """
    if request.method == 'POST':
        # Get Event and convert JSON description to python dict
        try:
            event = Event.objects.get(event_id=eventid)

        except Event.DoesNotExist:
            msg = f'The given Event with id {eventid} does not exist.'
            return JsonResponse({'error': msg}, status=404)

        # Go through request and update event
        event_dict = json.loads(event.description)
        body = json.loads(request.body)

        if body:
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
            event.start_date = event_dict['start']['utc']
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

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418
    msg = 'This endpoint is used for POST request and only accepts ' \
        + 'JSON objects. If you are seeing this error, then you either ' \
        + 'did not make a POST request or forgot to send the POST in the ' \
        + 'body of the request as a JSON object.'

    return JsonResponse({
        'Error': "I'm a teapot",
        'message': msg,
    }, status=418)
