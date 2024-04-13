from time import sleep
from celery import shared_task

@shared_task
def notify_customer(message):
    print('sending 10k email')
    print(message)
    sleep(10)
    print('email are send sucessfully')