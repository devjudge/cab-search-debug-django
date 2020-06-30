# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework import status
from restapi.models import validate_number, Driver, DriverLocation
from django.core.validators import validate_email
from math import radians, cos, sin, asin, sqrt

# Create your views here.


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def register_driver(request):
    try:
        if request.method == "POST":

            body = json.loads(request.body.decode('utf-8'))

            name = body.get('name', None)
            email = body.get('email', None)
            phone_number = body.get('phone_number', None)
            license_number = body.get('license_number', None)
            car_number = body.get('car_number', None)

            if body is None or name is None or email is None or phone_number is None or license_number is None or car_number is None:
                raise Exception("Value can't be None.")

            validate_email(email)
            validate_number(phone_number)

            db = Driver(name=name, email=email, phone_number=phone_number, license_number=license_number, car_number=car_number)
            db.save()

            u = Driver.objects.get(email=email)
            body['id'] = u.id

            return JsonResponse(body, status=status.HTTP_201_CREATED)

    except Exception as e:

        error = {"status": "failure", "reason": str(e)}
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)


def register_location(request, id):
    try:
        if request.method == 'POST':
            body = json.loads(request.body.decode('utf-8'))
            latitude = body.get('latitude', None)
            longitude = body.get('longitude', None)

            if latitude is None:
                raise Exception("Got null value for latitude.")
            if longitude is None:
                raise Http404("Got null value for latitude.")

            mydb = Driver.objects.get(id=id)
            db = DriverLocation(latitude=latitude, longitude=longitude, driver=mydb)
            db.save()
            return HttpResponse(status=status.HTTP_202_ACCEPTED)

    except Exception as e:
        error = {"status": "failure", "reason": str(e)}
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)


def get_available_cabs(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        latitude = body.get('latitude')
        longitude = body.get('longitude')
        if latitude is None or longitude is None:
            raise Exception("Got null value for either of longitude or latitude.")
        driver_locations = list(DriverLocation.objects.all())
        data = {'available_cabs': []}
        for location in driver_locations:
            distance = haversine(float(longitude), float(latitude), location.longitude, location.latitude)
            if distance < 4:
                data['available_cabs'].append({'name': location.driver.name, 'car_number': location.driver.car_number, 'phone_number': location.driver.phone_number})
        if len(data['available_cabs']) == 0:
            data = {"message": "No cabs available!"}
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data, status=status.HTTP_200_OK)

    except Exception as e:

        error = {"status": "failure", "reason": str(e)}
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)