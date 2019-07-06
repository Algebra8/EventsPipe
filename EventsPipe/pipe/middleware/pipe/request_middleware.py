from django.http import JsonResponse
import json

class RequestValidation:
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            print("Helllllooo")

        else:
            print('NOT POST')
        return view_func(request, *view_args, **view_kwargs)

class HeaderValidation:
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            if request.META['HTTP_X_AUTH'] != 'GENERIC_AUTH_KEY':
                # Return 401 UNAUTHORIZED
                status_code = 401
                msg = "Unauthorized request."
                exp = "User is unauthorized to access this request. Make sure " \
                + "x-auth header key is set to the required value."
                return JsonResponse(
                    {'message': msg, 'explanation': exp},
                    status=status_code,
                )

        return view_func(request, *view_args, **view_kwargs)
