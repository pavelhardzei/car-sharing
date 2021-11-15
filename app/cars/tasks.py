from celery import shared_task

from django.core.mail import send_mail
from .models import Car, CarInfo
from .serializers import CarSerializer
from django.conf import settings
from collections import OrderedDict


def compose(data):
    msg = []
    for car in data:
        indent = ['']
        stack = [[(k, v) for k, v in car.items()]]
        while len(stack) != 0:
            if not isinstance(stack[-1][0][1], OrderedDict):
                msg.append(f'{"".join(indent)}{stack[-1][0][0]}: {stack[-1][0][1]}')
                i = -1
            else:
                msg.append(f'{"".join(indent)}{stack[-1][0][0]}:')
                stack.append([(k, v) for k, v in stack[-1][0][1].items()])
                i = -2
                indent.append('\t')
            stack[i].pop(0)
            if len(stack[i]) == 0:
                stack.pop(i)
                indent.pop()
        msg.append('\n')

    return '\n'.join(msg)


@shared_task
def periodic_task():
    cars = Car.objects.select_related('car_info').filter(car_info__status=CarInfo.Status.broken)
    cars_ser = CarSerializer(cars, many=True)

    send_mail('Report', f'\tBroken cars:\n\n{compose(cars_ser.data)}', from_email=settings.EMAIL_HOST_USER, recipient_list=settings.RECIPIENT_LIST)
