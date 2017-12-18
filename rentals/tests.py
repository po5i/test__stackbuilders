# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import json
import datetime
from rentals.models import CarType, Car, Rental, RentalDates


class RentalTestCase(TestCase):

    def setUp(self):
        """ 
        Setup the initial data
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
        
        # Input data
        # {
        #     "rentDates": ["2017-11-19T05:00:00.000Z", "2017-11-20T05:00:00.000Z", "2017-11-21T05:00:00.000Z"],
        #     "car": {
        #         "model": "Cherato",
        #         "type": "sport"
        #     },
        #     "membership": false,
        #     "age": 24
        # }
        sample_data =  '{"rentDates":["2017-11-19T05:00:00.000Z","2017-11-20T05:00:00.000Z","2017-11-21T05:00:00.000Z"],"car":{"model":"Cherato","type":"sport"},"membership":false,"age":24}'
        parsed_data = json.loads(sample_data)
        car = Car.objects.get(model=parsed_data["car"]["model"])
        self.__class__.rental = Rental.objects.create(car=car, membership=parsed_data["membership"], age=parsed_data["age"])
        
        for date_str in parsed_data["rentDates"]:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            RentalDates.objects.create(rental=self.__class__.rental, date=date)

    def test_01_no_discount(self):
        """
        Simple sum of prices
        sport model x 3 days = 60 x 3 = 180
        """
        rental = self.__class__.rental
        self.assertEqual(rental.calculate_price(),180)


    def test_02_weekday_discount(self):
        """
        Allow for a discount on weekdays (10%).
        Two days of three
        """
        rental = self.__class__.rental
        price = rental.calculate_price() * (1 - rental.calculate_discount_weekday())
        self.assertEqual(price,168)

    def test_03_3_days_discount(self):
        """
        Allow for a discount for number of rental days (3 or more). 
            For 3 to 5 days 5%.
            For 6 to 10 days 10%
            11 or more 15%
        """
        rental = self.__class__.rental
        price = rental.calculate_price() * (1 - rental.calculate_discount_weekday())
        price *= 1 - rental.calculate_discount_by_number_of_days()
        self.assertEqual(price, 159.6)

    def test_04_membership_discount(self):
        """
        Differentiate price for people subscribed to a membership plan (5%).
        """
        rental = self.__class__.rental

        price = rental.calculate_price() * (1 - rental.calculate_discount_weekday())
        price *= 1 - rental.calculate_discount_by_number_of_days()
        price = price * (1 - rental.calculate_discount_membership())
        self.assertEqual(price, 159.6)

    def test_05_generate_insurance(self):
        """
        Get the insurance total
        3 days, sport, under age 24 = (7 * 3) + 25% = 26.25
        """
        rental = self.__class__.rental
        self.assertEqual(rental.calculate_insurance(), 26.25)

    def test_06_generate_total_discounts(self):
        rental = self.__class__.rental
        self.assertEqual(rental.calculate_total_discounts(), 0.11666666666666665)

    def test_07_total(self):
        rental = self.__class__.rental
        output = rental.generate_output()
        self.assertEqual(output["totalPayment"], 185.25)


# NOTE: this values (as they are in the email, does not match to the input data)
# Simply by calculating 3 days in sport car = 60 * 3 = 180 but here it says 350
# Am I missing something?

# {
#    "subtotal":350,
#    "insuranceTotal":53,
#    "discountPercentage":22.5,
#    "totalPayment":324.25
# }
