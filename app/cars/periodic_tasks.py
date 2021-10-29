from celery import shared_task


@shared_task
def periodic_task():
    from django.core.mail import send_mail
    from .models import Car, CarInfo
    from .serializers import CarSerializer
    from django.conf import settings

    cars = Car.objects.select_related('car_info').filter(car_info__status=CarInfo.Status.broken)
    cars_ser = CarSerializer(cars, many=True)

    send_mail('Report', f'Broken cars:\n {cars_ser.data}', from_email=settings.EMAIL_HOST_USER, recipient_list=['pavelgordei11@gmail.com'])
