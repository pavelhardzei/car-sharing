from rest_framework.exceptions import ValidationError


class ParseRequestMixin:
    def parse(self, request, fields):
        params = {}
        for field in fields:
            if field not in request.data:
                raise ValidationError({'error_message': f'{field} is required'})
            params[field] = request.data[field]

        return params
