# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class CarType(models.Model):
    name = models.CharField(max_length=64)
    rate = models.FloatField()
    insurance = models.FloatField()

class Car(models.Model):
    model = models.CharField(max_length=64)
    type = models.ForeignKey(CarType)

class Rental(models.Model):
    car = models.ForeignKey(Car)
    membership = models.BooleanField()
    age = models.IntegerField()

    def calculate_price(self):
        days = self.dates.all().count()
        return self.car.type.rate * days

    def calculate_discount_weekday(self):
        sum = 0
        for rental_date in self.dates.all():
            if rental_date.date.weekday() in range(0, 4):
                sum += (self.car.type.rate * 0.9)
            else:
                sum += self.car.type.rate
        difference = sum / self.calculate_price()
        return 1 - difference

    def calculate_discount_by_number_of_days(self):
        """
        Allow for a discount for number of rental days (3 or more). 
            For 3 to 5 days 5%.
            For 6 to 10 days 10%
            11 or more 15%
        """
        days = self.dates.all().count()
        if days >= 3 and days <=5:
            return 0.05
        elif days >= 6 and days <= 10:
            return 0.1
        elif days > 11:
            return 0.15

    def calculate_discount_membership(self):
        """
        Differentiate price for people subscribed to a membership plan (5%).
        """
        if self.membership:
            return 0.05
        else:
            return 0


    def calculate_insurance(self):
        """
        Generate an insurance policy and differentiate its price for people younger than 25 years old. 
            5USD a day for the small car
            7USD a day for the sport car
            10USD a day for the SUV 
            with a 25% increase for younger people. 
            No discount applies over the insurance total.
        """
        days = self.dates.all().count()
        insurance = self.car.type.insurance * days

        if self.age > 25:
            return insurance
        else:
            return insurance * 1.25


    def calculate_total_discounts(self):
        return self.calculate_discount_weekday() + self.calculate_discount_by_number_of_days() + self.calculate_discount_membership()

    def generate_output(self):
        """
        Get the final output
        """
        
        # Make sure that the person renting the car is at least 18 years old.
        if self.age < 18:
            raise
            
        subtotal = self.calculate_price()
        insurance = self.calculate_insurance()
        discounts = self.calculate_total_discounts()
        total = (subtotal * (1 - discounts)) + insurance

        return {
            "subtotal": subtotal,
            "insuranceTotal": insurance,
            "discountPercentage": discounts,
            "totalPayment": total
        }

class RentalDates(models.Model):
    rental = models.ForeignKey(Rental, related_name='dates')
    date = models.DateTimeField()