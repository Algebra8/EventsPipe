import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventsPipe.settings')
django.setup()

import requests
import json
from django.utils.dateparse import parse_datetime

from pipe.models import Event



# Eventbrite Events API call
url = "https://www.eventbriteapi.com/v3/events/search"

# Private OAuth header
pOAuth = os.getenv("PRIV_OAuth")

# Header for OAuth
headers = {
  "Authorization": f"Bearer {pOAuth}",
  "Content-Type": "application/json",
}


def get_events(url, headers):
    print("Getting events...")
    response_json = requests.get(url, headers=headers).json()
    return response_json['events']
    print("Got events.")


def parse_event_startdate(start_date: string):
    return parse_datetime(start_date)


def populate_events_db(events_input):
    print("Populating Events database...")
    for ev in events_input:
        event = Event()
        # Event description is json dumps
        event.description = json.dumps(ev)
        event.name = ev['name']['text']
        event.event_id = ev['id']
        event.start_date = parse_event_startdate(ev['start']['utc'])
        event.save()

    print("Events database populated with events.")

def scrape_events(n_pages: int):
    page_num = 1
    events = []
    # Do for each page
    for _ in range(n_pages):

        # Concatenate events to events
        page_url = url + f"?page={page_num}"
        events += get_events(page_url, headers)

        # Go through events and populate db
        populate_events_db(events)

        # Increment page number
        page_num += 1

        # Reset page_url
        page_url = url


if __name__ == '__main__':
    scrape_events(1)
