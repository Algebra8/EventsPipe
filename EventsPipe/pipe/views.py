from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
import json

from pipe.models import Event, Ticket

def index(request):
    html = "<h1>goobye wordle</h1>"
    return HttpResponse(html)


def get_event_by_name(request, event_name):
    ev = Event.objects.get(name=event_name)
    data = json.loads(ev.description)

    return JsonResponse(data)


def get_event_by_id(request, eventid):
    ev = Event.objects.get(event_id=int(eventid))
    data = json.loads(ev.description)

    return JsonResponse(data)


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
