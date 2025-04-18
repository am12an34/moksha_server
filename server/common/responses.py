from rest_framework.response import Response


class NoContentResponse(Response):
    status_code = 204
    default_code = 'no_content'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
