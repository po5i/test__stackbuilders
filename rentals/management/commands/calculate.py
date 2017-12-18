from django.core.management.base import BaseCommand, CommandError
from rentals.models import *
import json
import datetime

class Command(BaseCommand):
    help = 'Usage example:  python manage.py calculate \'{"rentDates":["2017-11-19T05:00:00.000Z","2017-11-20T05:00:00.000Z","2017-11-21T05:00:00.000Z"],"car":{"model":"Cherato","type":"sport"},"membership":false,"age":24}\''

    def add_arguments(self, parser):
        parser.add_argument('json', type=str)

    def handle(self, *args, **options):
        """
        Input a json, and get a json
        """
        parsed_data = json.loads(options["json"])
        car = Car.objects.get(model=parsed_data["car"]["model"])
        rental = Rental.objects.create(car=car, membership=parsed_data["membership"], age=parsed_data["age"])
        
        for date_str in parsed_data["rentDates"]:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            RentalDates.objects.create(rental=rental, date=date)

        output = json.dumps(rental.generate_output(), ensure_ascii=False)

        self.stdout.write('===================================================')
        self.stdout.write(output)
        self.stdout.write('===================================================')
        self.stdout.write('Completed!')
        rental.delete()
