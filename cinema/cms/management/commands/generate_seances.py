from datetime import timedelta
from django.core.management.base import BaseCommand
from cms.models import Seance, Movies, Halls
from django.utils.datetime_safe import datetime, time
from random import choice


class Command(BaseCommand):
    help = 'Generates seances for a week'

    date_range = [datetime.now().date() + timedelta(days=day) for day in range(7)]
    time_range = [(datetime.combine(datetime.now(), time(10, 0)) + timedelta(hours=i)).time() for i in range(14)]
    list_halls = [hall.id for hall in Halls.objects.all()]
    list_movies = [movie.id for movie in Movies.objects.filter(date_premier__lte=datetime.now(), active=True)]

    def handle(self, *args, **options):
        for day in self.date_range:
            Seance.objects.filter(date=day).delete()
            for _time in self.time_range:
                Seance.objects.get_or_create(
                    date=day,
                    time=_time,
                    ticket_price=choice([90, 100, 110, 120, 130]),
                    halls_id=choice(self.list_halls),
                    movies_id=choice(self.list_movies)
                )
        self.stdout.write('Successfully generated seances')
