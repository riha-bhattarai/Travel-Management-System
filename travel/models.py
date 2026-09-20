from django.db import models
from django.contrib.auth.models import User



class TourPackage(models.Model):

    package_name = models.CharField(
        max_length=100
    )

    destination = models.CharField(
        max_length=100
    )

    description = models.TextField()

    itinerary = models.TextField(
        blank=True
    )

    duration = models.CharField(
        max_length=50
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    available_seats = models.IntegerField()

    start_date = models.DateField()

    transportation = models.CharField(
        max_length=50,
        default='Tourist Bus'
    )

    accommodation = models.CharField(
        max_length=100,
        blank=True
    )

    meals = models.CharField(
        max_length=100,
        blank=True
    )

    sightseeing = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.package_name


class Booking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    customer_name = models.CharField(
        max_length=100
    )

    customer_email = models.EmailField()

    tour_package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE
    )

    booking_date = models.DateField(
        auto_now_add=True
    )

    number_of_people = models.IntegerField()

    transportation_upgrade = models.CharField(
        max_length=50,
        default='None'
    )

    transportation_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    def __str__(self):
        return self.customer_name



class Payment(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50
    )

    payment_date = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    def __str__(self):
        return str(self.booking)