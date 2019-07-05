import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventsPipe.settings')
django.setup()

import requests
import json
from pipe.models import Event, Ticket

# Eventbrite Tickets API call
# url = f"https://www.eventbriteapi.com/v3/events/{event_id}/ticket_classes/"

# Private OAuth header
pOAuth = os.getenv("PRIV_OAuth")

# Header for OAuth
headers = {
  "Authorization": f"Bearer {pOAuth}",
  "Content-Type": "application/json",
}


def get_tickets(url, headers):
    """
    Function that uses the given url and headers
    to return a list of tickets per event. The url
    will contain the event for the given list of tickets.
    """
    print("Getting tickets...")
    response_json = requests.get(url, headers=headers).json()
    return response_json['ticket_classes']

def populate_tickets_db(ticket_input, event_input):
    """
    Function to populate the Ticket model using the
    list of tickets and an Event object. The Event
    object is a ForeignKey in the Ticket model.

    `ticket_input`: List of tickets per event
    `event_input`: Event object
    """
    print("Populating Tickets database...")
    N_tickets_per_event = len(ticket_input)
    for i in range(N_tickets_per_event):
        ticket = Ticket()
        if 'cost' in ticket_input[i]:
            ticket.ticket_cost = float(ticket_input[i]['cost']['major_value'])
            ticket.event_id = event_input
            ticket.save()
        else:
            ticket.ticket_cost = float(0)
            ticket.event_id = event_input
            ticket.save()

    print("Tickets database populated with new ticket.")

def scrape_tickets(events):
    """
    Function to scrape tickets from a list of Event objects.

    `events`: List of Event objects
    """
    print("Beginning Ticket scraping...")
    # For each event, use event_id to find ticket and event to populate db
    for event in events:
        """
        `tickets` is a list containing all the different tickets for
        any single event. An event can have one or more tickets and therefor,
        one or more ticket costs.
        """
        # Search for ticket
        event_id = event.event_id
        url = f"https://www.eventbriteapi.com/v3/events/{event_id}/ticket_classes/"
        tickets = get_tickets(url, headers)
        # Populate db with ticket
        populate_tickets_db(tickets, event)

    print("Ticket scraping completed.")



if __name__ == '__main__':
    # Call Events object
    events = Event.objects.all()
    # Scrape tickets and populate database
    scrape_tickets(events)
