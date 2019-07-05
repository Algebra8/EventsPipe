import os
import json
import requests

pOAuth = "4GQQFB6MUA5Y2RNBIQ55"

headers = {
  "Authorization": f"Bearer {pOAuth}",
  "Content-Type": "application/json",
}

event_id = 52606110292

url = f"https://www.eventbriteapi.com/v3/events/{event_id}/ticket_classes/"

response_json = requests.get(url, headers=headers).json()

# 'ESL One Cologne 2019'
tickets_for_ESL = response_json['ticket_classes']

]
tickets_for_ESL[6]

a = {"a": 5, "b": 10}

vv = json.dumps(a)

vv

tt = json.loads(vv)
tt
# NOTE: If a user asks for an event that costs $33,
# then what should be returned? The json of the entire
# event that it was a part of? Or the ticket?

# Note that tickets_for_ESL[6] is a sub-event of the
# ESL One Cologne 2019 event. So, which do I send back?

# I could dump that specific entire sub-event into the
# ticket object as I did with the events objects.


organization_id = 25399112885
url_org = f"https://www.eventbriteapi.com/v3/organizations/{organization_id}/roles/"
org = requests.get(url_org, headers=headers)

org


url_event = "https://www.eventbriteapi.com/v3/events/search/"

ev = requests.get(url_event, headers=headers)
e = ev.json()
e = e['events']

# path("events/name/<str:event_name>", views.get_event_by_name, name="get_event_by_name"),
# path("events/id/<int:eventid>", views.get_event_by_id, name="get_event_by_id"),
# path("events/cost/<str:cost>", views.get_events_by_cost, name="get_events_by_cost"),
