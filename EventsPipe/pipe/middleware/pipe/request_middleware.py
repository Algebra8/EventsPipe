from django.http import JsonResponse
from pipe.models import Event
import json


class HeaderValidation:
    def process_view(self, request, view_func, view_args, view_kwargs):
        msg = "Unauthorized or Bad request."
        exp = "User is unauthorized to access this request or  " \
        + "has not provided a required header. Make sure " \
        + "x-auth header key is set to the required value."

        if request.method == "POST":
            if not 'X-Auth' in request.headers:
                # Return 400 BAD REQUEST
                status_code = 400
                return JsonResponse(
                    {'message': msg, 'explanation': exp},
                    status=status_code,
                )

            if request.headers['X-Auth'] != 'GENERIC_AUTH_KEY':
                # Return 401 UNAUTHORIZED
                status_code = 401
                return JsonResponse(
                    {'message': msg, 'explanation': exp},
                    status=status_code,
                )

        return view_func(request, *view_args, **view_kwargs)
