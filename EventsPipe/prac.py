# @csrf_exempt
# @decorator_from_middleware(HeaderValidation)
# def update_event(request, eventid):
#     if request.method == 'POST':
#         # Form
#         event_form = EventForm(request.POST)
#         if event_form.is_valid():
#             # Get Event and convert JSON description to python dict
#             event = Event.objects.get(event_id=eventid)
#             event_dict = json.loads(event.description)
#
#             # Go through request and update event
#             if request.body:
#                 body = json.loads(request.body)
#
#                 # Check if JSON request is valid
#                 not_valid = request_validation(body, event_dict)
#                 if not_valid:
#                     return not_valid
#
#                 # Update Event JSON
#                 for key, val in body.items():
#                     event_dict[key] = val
#
#             # Update fields of Event object
#             event.name = event_dict['name']
#             print("------------------------------")
#             event.event_id = event_dict['id']
#             print("------------------------------")
#             event.start_date = parse_datetime(event_dict['start']['utc'])
#
#             # Convert object back to JSON and place in event
#             event.description = json.dumps(event_dict)
#
#
#             # Note django will automatically update
#             # the object if pk is an existing value
#             event.save()
#
#             return JsonResponse(json.loads(event.description))
#
#         else:
#             return HttpResponse("Not valid")
#
#     return HttpResponse("Didn't get it...")









# Views

# def get_event_by_name(request, event_name):
#     ev = Event.objects.get(name=event_name)
#     data = json.loads(ev.description)
#
#     return JsonResponse(data)


# def get_event_by_id(request, eventid):
#     ev = Event.objects.get(event_id=int(eventid))
#     data = json.loads(ev.description)
#
#     return JsonResponse(data)
