from django.urls import path
from learn_celery.views import add_value_in_celery, send_test_email

urlpatterns = [
    path('add-value', add_value_in_celery, name='add_value'),
    path('send-email', send_test_email, name='send_email')
]