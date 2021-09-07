from django.http import HttpResponse


def health(request):
    return HttpResponse('OK', status=status.HTTP_200_OK)

