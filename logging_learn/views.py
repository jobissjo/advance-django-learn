from django.shortcuts import render
from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)

# Create your views here.


def home(_request):
    logger.info('Home Page accessed')
    return JsonResponse({"message": "This is django's home page"})

def check_all_logs(_request):
    logger.info('this is testing log errror')
    logger.error('just testng error log')
    logger.warning("this is testing waring log")
    logger.debug("this is testing debug log")
    logger.critical("just testng debug log of critical")

    return JsonResponse({'message': "All the logs created by this test"})