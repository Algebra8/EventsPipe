from django.http import JsonResponse


def request_validation(request_body, event_dict):
    # Check for valid keys
    for key, val in request_body.items():
        if key not in event_dict:
            # Return 400 BAD REQUEST
            status_code = 400
            msg = "Server could not understand the request."
            exp = "Bad input given for request. {key} is not a key in " \
                + "in any Event."

            return JsonResponse(
                {'message': msg, 'explanation': exp},
                status=status_code,
            )

    # Continue route
    return
