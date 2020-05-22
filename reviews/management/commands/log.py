import django_rq
import logging
from datetime import datetime, timedelta
import time


from django.core.management.base import BaseCommand
from django_rq import job
from reviews.models import Review

#@job
def get_count_reviews():
    logger = logging.getLogger('counter')
    count = Review.objects.count()
    time.sleep(4)
    if count:
        logger.info(f'Всего отзывов в системе: {count}')
    else:
        logger.error('Something went wrong!')

class Command(BaseCommand):
    help = "Выводит на экран и в лог количество записей в таблице Review"

    def handle(self, *args, **options):
        scheduler = django_rq.get_scheduler('default')
        scheduler.schedule(
            scheduled_time=datetime.now(), 
            func=get_count_reviews,
            interval=10,
            repeat=4,
        )
