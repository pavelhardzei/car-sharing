from rest_framework.exceptions import ValidationError


class QueryParamsMixin:
    def query_params(self, request, keys):
        params = {}
        for key in keys:
            if key not in request.query_params:
                raise ValidationError({'error_message': f'{key} is required'})
            params[key] = request.query_params[key]

        return params
