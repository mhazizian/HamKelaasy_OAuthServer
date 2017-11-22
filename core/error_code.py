from enum import Enum


class Error_code(object):
    class Phone_number(Enum):
        Server_in_development = 1005
        Server_is_busy = 1006
        Invalid_number = 1001


errors = {
    Error_code.Phone_number.Server_in_development.value: {
        'message': 'Sms server is in development, please try again later',
        'status': 503
    },
    Error_code.Phone_number.Server_is_busy.value: {
        'message': 'Sms server is busy, try again later.',
        'status': 503
    },
    Error_code.Phone_number.Invalid_number.value: {
        'message': 'Invalid phone number',
        'status': 400
    },
}
