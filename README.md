### **Intro**

The EventsPipe project is a backend application that allows users to query or update events from a predefined set of Eventbrite events. Queries can be done based on event name, start date, or ticket cost while updates, in the form of POST requests, are accessed with an event's id.

### **Usage**

##### Query

To query an event, access the API with the domain access and the **events/search** endpoint. No headers or special authorization is required. Events are returned as JSON objects.

```
url: domain_name`/pipe/events/search/
```

Given no query parameters, the `search` endpoint will yield a JSON object that contains all of the events that exist in the database.

Use query parameters to search for an event. The list of query parameters and their types are given in the table below.

<table
  style="font-family: arial, sans-serif;
border-collapse: collapse;
width: 100%;"
>
  <thead>
    <th>keys</th>
    <th>types</th>
    <th>returns</th>
  </thead>
  <tr>
    <td>event_name</td>
    <td>string</td>
    <td>Event with given event name</td>
  </tr>
  <tr>
    <td>ticket_cost</td>
    <td>float or integer</td>
    <td>Multiple Events with given ticket cost</td>
  </tr>
  <tr>
    <td>start_date</td>
    <td>string, format: YYYY-MM-DD</td>
    <td>Events with given start dates</td>
  </tr>
</table>

> Example Query:
> domain/pipe/events/search/?event_name=ATLANTA'S #1 ROOFTOP DAY PARTY

##### Update

This API uses POST requests to update a given event. To update the event, the user is expected to have the appropriate authentication in the form of a header value with the key `x-auth`.

```
url: `domain_name`/pipe/events/update/<id:eventid>

```

> Note that due to the privilege that the user is expected to have in order to update an event, i.e. the `x-auth` token, it is assumed that the user knows the event's id beforehand and the event fields' key, value pairs that it wants to update.

### **Explanation of Methodologies**

##### Date Scraping

In order to populate the database, public events were scraped from the Eventbrite API using the modules `event_scraper.py` and `ticket_scraper.py`, both of which have a procedural paradigm. As can be deduced from their names, the former module was used to scrape the required events while the latter was used to scrape data on their respective ticket costs. The applications database contains above 500 Eventbrite Events and over 2000 references to Eventbrite Ticket objects. For more information regarding Eventbrite API's Event and Ticket objects, please refer to their [API Reference](https://www.eventbrite.com/platform/api) page.

In order to re-populate the database using the `event_scraper` and `ticket_scraper` modules,
it is necessary to first clear the database and previous migrations, run the
`event_scraper` module with the desired Eventbrite Event pages to scrape, and finally run
the `ticket_scraper` module.

```
> $ python event_scraper.py
> How many pages of Eventbrite Events would you like to scrape?
>>> 3
> $ python ticket_scraper.py
```

> Each Eventbrite Event page contains roughly 50 public Events.

##### Models

This application makes use of Django's in-built SQLite database engine. A breakdown of the modules is given below.

<table
  style="font-family: arial, sans-serif;
border-collapse: collapse;
width: 100%;"
>
  <thead>
    <th>model</th>
    <th>field</th>
    <th>type</th>
  </thead>
  <tr>
    <td>Event</td>
    <td><ul style="list-style: none;">
      <li>description</li>
      <li>name</li>
      <li>event_id</li>
      <li>start_date</li>
    </ul></td>
    <td><ul style="list-style: none;">
      <li>TextField</li>
      <li>CharField</li>
      <li>IntegerField</li>
      <li>DateTimeField, TZ=True</li>
    </ul></td>
  </tr>
  <tr>
    <td>Ticket</td>
    <td><ul style="list-style: none;">
      <li>ticket_cost</li>
      <li>event</li>
    </ul></td>
    <td><ul style="list-style: none;">
      <li>FloatField</li>
      <li>Event</li>
    </ul></td>
  </tr>
</table>

While most of the fields in each model are self-descriptive, one notable one is `Event.description`. The Eventbrite API's Event object contained many fields. Therefore, in order to allow updating of the object, either the applications Event model would have to mirror Eventbrite's Event model or the applications Event model could hold each respective Everbrite Event object as a json object. The latter would allow the application to access the fields the user wished to update by converting the JSON object to a Python dictionary using the `json.loads` function. Since many of the Eventbrite model's fields included other custom Eventbrite models, the first method was not a feasible choice, and so, this application took the second route.

Custom model validation was created and can be viewed in the `pipe/validators` directory.

##### Views

The backend controller (in `views.py`) contains two API endpoints. **events/search/** and **events/update/<int:eventid>** are handled by `views.get_event` and `views.update_event`, respectively. The controllers make heavy use of utility functions and middleware, which exist in `pipe/middleware` and `pipe/utils`.

It is worth mentioning that Eventbrite Tickets have an interesting structure. Due to the fact that each Event may have multiple 'sub-events' (such as a Saturday entrance or Sunday entrance at a festival), it is likely that each sub-event has its own ticket cost. Therefore, when searching for an event based on the ticket cost, i.e. with the `ticket_cost` query parameter, it is likely that some of the events returned may be duplicates. This is dealt with by filtering and returning distinct Events when searching by cost. The user can be expected to use this information to then search for the sub-event of their liking, knowing that within that event there exists some sub-event with the wanted ticket price. For more details on filtering and returning distinct events, please refer to the function `pipe.utils.get_events_by_cost`.

##### Tests

Tests exist in the `pipe/tests` directory and contain testing for both Event and Ticket models in `test_models.py`, as well as testing of GET and POST operations for the controller in `test_views.py`.

### **Miscellaneous**

The `x-auth` token's required value is `GENERIC_AUTH_KEY`.

A quick rundown of some of the things I would do differently next time:

<ul>
    <li>Make the models fat and the views thin, a good example of which is <a href="https://github.com/django/django/blob/ff6ee5f06c2850f098863d4a747069e10727293e/django/contrib/auth/models.py#L225-404"> this example code</a> of Django's own model's structure. </li>

    <li>
    Add regex support for searching by event name.
    </li>

</ul>
