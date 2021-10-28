from celery import shared_task


@shared_task
def periodic_task():
    with open('testing.txt', 'a') as file:
        file.write('test')
