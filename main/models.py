from random import randint
from django.db import models


def random_car_number() -> int:
    """Generate a unique number of 4 digits for -> Car.car_number"""
    not_unique = True
    while not_unique:
        unique_num = randint(1000, 9999)
        if not Car.objects.filter(car_number=unique_num):
            not_unique = False
    return unique_num


class Car(models.Model):
    """Car instance"""
    car_model = models.CharField(max_length=255)
    car_number = models.IntegerField(unique=True, default=random_car_number)
    rent_cost_per_day = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.car_model


class DocumentStatusChoises:
    """Document statuses"""
    FINISHED = "Finished"
    IN_PROGRESS = "In progress"
    EXPIRED = "Expired"

    CHOICES = (
        (FINISHED, "Finished"),
        (IN_PROGRESS, "In progress"),
        (EXPIRED, "Expired"),
    )


class Document(models.Model):
    """Document instance"""
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    renting_date_from = models.DateField()
    renting_date_to = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=DocumentStatusChoises.CHOICES,
                              max_length=255,
                              default=DocumentStatusChoises.IN_PROGRESS)

    def __str__(self) -> str:
        return 'Document ID: {}'.format(self.id)

    def client_full_name(self) -> str:
        """Return full name"""
        return '{} {}'.format(self.first_name, self.last_name)

    def get_total_rent_days(self) -> str:
        """Return amount of days the car to be rented"""
        return self.renting_date_to - self.renting_date_from

    def get_total_rent_price(self):
        """Return total amount client has to pay for rent"""
        lst = str(self.get_total_rent_days()).split(' ')
        return int(lst[0]) * self.car.rent_cost_per_day
