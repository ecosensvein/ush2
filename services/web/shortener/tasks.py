from shortener.models import Url
from django.conf import settings
from celery import task
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@task(name='purge')
def purge_old_redirects():
    '''Removes old redirect rules from db'''
    deletion = Url.objects.filter(created_at__lte=datetime.now() -
                                  timedelta(seconds=settings.DB_TTL)).delete()
    logger.info('PURGE FOR %s OLD REDIRECTS' % deletion[0])
