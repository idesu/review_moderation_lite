import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Review


class Command(BaseCommand):
    help = "Выводит на экран и в лог количество записей в таблице Review"

    def handle(self, *args, **options):
        count = Review.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))} Всего отзывов в системе: {count}'
            )
        )
        with open(f"count.log", "a") as f:
            f.write(
                f'{str(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))} Всего отзывов в системе: {count}\n'
            )
