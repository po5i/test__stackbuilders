from django.core.management.base import BaseCommand, CommandError
from rentals.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Initialize sample data
        """
        # 40USD/day for small cars
        # 60USD/day for sport cars
        # 100USD/day for SUV cars).
        small = CarType.objects.create(name="small", rate=40.0, insurance=5)
        sport = CarType.objects.create(name="sport", rate=60.0, insurance=7)
        suv = CarType.objects.create(name="suv", rate=100.0, insurance=10)

        # Model: Dwarfy, Type: Small car
        # Model: Halfing, Type: Small car
        # Model: Eveo, Type: Sport car
        # Model: Cherato, Type: Sport car
        # Model: Vitoro, Type: SUV
        # Model: Exploring, Type: SUV
        Car.objects.create(model="Dwarfy", type=small)
        Car.objects.create(model="Halfing", type=small)
        Car.objects.create(model="Eveo", type=sport)
        Car.objects.create(model="Cherato", type=sport)
        Car.objects.create(model="Vitoro", type=suv)
        Car.objects.create(model="Exploring", type=suv)
        
        self.stdout.write('Completed')
