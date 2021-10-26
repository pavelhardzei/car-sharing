from rest_framework.exceptions import APIException
from rest_framework import status


class LogicError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail=None, status_code=None):
        if status_code:
            self.status_code = status_code
        if detail:
            self.detail = {'detail': detail}
        else:
            self.detail = {'detail': self.default_detail}
