from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
import re


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

@user_passes_test(lambda u: u.is_superuser)
def show_all_logs(request, filename):

    logger.info('Superuser only view accessed')
    if ".." in filename or "/" in filename or "\\" in filename:
        return JsonResponse({"error": "Invalid filename"}, status=400)
    
    log_path  = settings.BASE_DIR / 'logs' / filename

    log_level = request.GET.get('level', None)

    if not log_path .exists():
        return HttpResponse("Log File not found", status=404)
    
    filtered_logs = []
    with open(log_path , 'r') as f:
        for line in f:
            if not log_level or re.search(rf"\b{log_level}\b", line, re.IGNORECASE):
                filtered_logs.append(line)
    if not filtered_logs:
        return JsonResponse({"message": "No logs found for the given level"}, status=200)
    
    return HttpResponse("".join(filtered_logs), content_type='text/plain')

       