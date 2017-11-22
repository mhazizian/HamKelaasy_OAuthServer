import json
from core.error_code import errors
from django.http import HttpResponse


class HamkelaasyError(Exception):
    def __init__(self, error_code):
        self.error_code = error_code.value
        self.message = errors[error_code.value].get('message', '')
        self.status = errors[error_code.value].get('status', 400)

    def set_message(self, message):
        self.message = message

    def set_status_code(self, status_code):
        self.status = status_code

    def to_dictionary(self):
        return {
            'message': self.message,
            'code': self.error_code
        }

    def to_http_response(self):
        res = {'errors': [self.to_dictionary()]}
        return HttpResponse(
            unicode(json.dumps(res)),
            status=self.status,
            content_type='application/json',
        )
