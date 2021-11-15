from celery import shared_task

from django.core.mail import send_mail
from .models import Car, CarInfo
from .serializers import CarSerializer
from django.conf import settings
from collections import OrderedDict

@shared_task
def periodic_task():
    def compose(data):
        def parse(car, res):
            for k, v in car.items():
                if isinstance(v, OrderedDict):
                    parse(v, res)
                else:
                    res.append(f'{k}: {v}')
        msg = []
        for item in data:
            parse(item, msg)
            msg.append('\n')
        return '\n'.join(msg)

    cars = Car.objects.select_related('car_info').filter(car_info__status=CarInfo.Status.broken)
    cars_ser = CarSerializer(cars, many=True)

    send_mail('Report', f'\tBroken cars:\n\n{compose(cars_ser.data)}', from_email=settings.EMAIL_HOST_USER, recipient_list=settings.RECIPIENT_LIST)
