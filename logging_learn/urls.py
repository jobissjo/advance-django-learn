from django.urls import path
from logging_learn import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check-all-logs', views.check_all_logs, name='check-all-logs'),
    path('show-all-logs/<str:filename>', views.show_all_logs, name='show-all-logs'),

]