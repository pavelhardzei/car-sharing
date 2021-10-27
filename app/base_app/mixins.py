from rest_framework.exceptions import ValidationError


class BaseMixin:
    def action(self, request_dict, iter_items):
        params = {}
        for item in iter_items:
            if item not in request_dict:
                raise ValidationError({'error_message': f'{item} is required'})
            params[item] = request_dict[item]

        return params


class QueryParamsMixin(BaseMixin):
    def query_params(self, request, keys):
        return self.action(request.query_params, keys)


class ParseRequestMixin(BaseMixin):
    def parse(self, request, fields):
        return self.action(request.data, fields)
