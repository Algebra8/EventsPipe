from django.http import JsonResponse


def request_validation(request_body, event_dict):
    # Check for valid keys
    for key, val in request_body.items():
        if key not in event_dict:
            print("Key not in")
            # Return 400 BAD REQUEST
            status_code = 400
            msg = "Server could not understand the request."
            exp = "User is unauthorized to access this request. Make sure " \
            + "x-auth header key is set to the required value."

            return JsonResponse(
                {'message': msg, 'explanation': exp},
                status=status_code,
            )

    # Continue route
    return
