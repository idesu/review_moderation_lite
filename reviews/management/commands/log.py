import django_rq
import os
import time
from datetime import datetime
from django_rq import job


from django.core.management.base import BaseCommand

from reviews.models import Review


class Command(BaseCommand):
    help = "Выводит на экран и в лог количество записей в таблице Review"

    def handle(self, *args, **options):
        count = django_rq.enqueue(Review.objects.count)
        time.sleep(4)
        self.stdout.write(
            self.style.SUCCESS(
                f'{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))} Всего отзывов в системе: {count.result}'
            )
        )
        with open(f"count.log", "a") as f:
            f.write(
                f'{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))} Всего отзывов в системе: {count.result}\n'
            )
