from django.http import HttpResponseForbidden
from common.exceptions import BadRequest
from functools import wraps


def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Unauthorized")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def body(fields: set[str]):
    """ Enforce what fields must be present in the request body """

    def _decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            fields_copy = fields.copy()

            for key in request.data:
                try:
                    fields_copy.remove(key)
                except KeyError:
                    raise BadRequest(message=f'{key} should not be present in request body')

            for field in fields_copy:
                raise BadRequest(message=f'{field} is required')

            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return _decorator
