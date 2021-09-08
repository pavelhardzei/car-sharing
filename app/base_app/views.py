from django.http import HttpResponse
from rest_framework import status


def health(request):
    return HttpResponse('OK', status=status.HTTP_200_OK)
