from celery import shared_task


@shared_task
def periodic_task():
    from .models import Car, CarInfo
    from .serializers import CarSerializer

    cars = Car.objects.select_related('car_info').filter(car_info__status=CarInfo.Status.broken)
    cars_ser = CarSerializer(cars, many=True)
    with open('report.txt', 'w') as file:
        if cars.count():
            file.write(f'Broken cars: {cars_ser.data}')
        else:
            file.write('Everything is ok')
