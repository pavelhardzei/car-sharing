from django.http import HttpResponse


def health(request):
    return HttpResponse('OK', status=200)