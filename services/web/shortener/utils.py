from django.http import JsonResponse
from shortener.models import Url
import random
import string
import logging

logger = logging.getLogger(__name__)


def generate_subpart_inner():
    '''Generates new random subpart'''
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated subpart_inner is used then generate next
    while True:
        subpart_inner = ''.join(random.choice(char) for x in range(length))
        if not Url.objects.filter(subpart_inner=subpart_inner).exists():
            return subpart_inner


def LoggingResponse(context, log_entry, **kw):
    '''Returns http json response'''
    logger.info(log_entry)
    return JsonResponse(context, **kw)
