# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import validate_email
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


def validate_number(number):
    print("validating number: {}".format(number))
    if len(str(number)) != 7:
        raise ValidationError("Number must be of 10 digit, number: {}.".format(number))


# Create your models here.
class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=254, validators=[validate_email], unique=True)
    phone_number = models.IntegerField(unique=True, validators=[validate_number])
    license_number = models.CharField(max_length=20, unique=True)
    car_number = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class DriverLocation(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.driver.name