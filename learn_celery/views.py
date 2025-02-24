from django.shortcuts import render
from learn_celery.tasks import add, send_email_task
from django.http import JsonResponse
from django.conf import settings

# Create your views here.

def add_value_in_celery(_request):
    add.delay(4,6)
    return JsonResponse({'message': 'value calculated in behind the scree'})

def send_test_email(_request):
    # TODO: Implement sending email using Celery
    send_email_task.delay('Testing Email', 'testing_email', {'username': 'Jobi'}, [settings.EMAIL_HOST_USER])
    print(settings.EMAIL_HOST_USER, 'Test Email')
    return JsonResponse({'message': 'Email sent'})
    