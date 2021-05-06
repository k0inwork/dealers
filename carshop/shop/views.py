from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from django.utils import timezone

from .models import Deal,Car,Dealer,CarModel
from .serializers import DealSerializer, CarSerializer

from rest_framework.exceptions import APIException

class ViewDeals(generics.ListCreateAPIView):
    serializer_class=DealSerializer

    def get_queryset(self):
        d = self.request.query_params.get('dealer')
        if d:
            return Deal.objects.filter(dealer__name=d)
        return Deal.objects.all()


class WrongRequestException(APIException):
    status_code = 401
    default_detail = "Wrong parameters provided"

#import logging
class SellCarView(generics.CreateAPIView):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    
    def perform_create(self, serializer):

#        logging.error("create"+str(self.request.data))

        carid = self.request.data.get('carid')

        if carid:
            try:
                car = Car.objects.get(id=carid)
            except Exception as ex:
                raise WrongRequestException(str(ex))

        else:
            raise WrongRequestException("Car id not valid")

        if not car.present:
            raise WrongRequestException("Car is not present for sale")


        dealername = self.request.data.get('dealer')
        if dealername:
            try:
                dealer = Dealer.objects.get(name=dealername)
            except Exception as ex:
                raise WrongRequestException(str(ex))
        else:
            raise WrongRequestException("Dealer not valid")

        realprice = self.request.data.get('price')
        date = self.request.data.get('date')

        if not date:
            date = timezone.now()
        
        if realprice:
            deal = serializer.save(car=car,dealer=dealer,realprice=realprice,date = date)
        else:
            deal = serializer.save(car=car,dealer=dealer,date = date)

        #Car is sold
        car.present=False
        car.save()

        return deal
            


class ViewAvailableCars(generics.ListCreateAPIView):
    serializer_class=CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['model__manufactorer__name', 'model__modelName','price']

    def get_queryset(self):

        price_range = self.request.query_params.get('pricerange')
        if not price_range:         
            return Car.objects.filter(present=True)

        try:
            pricer = price_range.split(",")
            pricelow = pricer[0]
            pricehigh = pricer[1]

            if pricelow=='':
                pricelow=0
            if pricehigh=='':
                pricehigh=9999999999

            return Car.objects.filter(present=True, price__gte=int(pricelow), price__lte=int(pricehigh))
        except Exception as ex:
            raise WrongRequestException(str(ex))
    
class CreateCar(generics.CreateAPIView):
    serializer_class=CarSerializer


    def perform_create(self, serializer):
        # model 

        modelName = self.request.data.get('model')
        year = self.request.data.get('year')
        if not modelName:
            raise WrongRequestException("Model not provided")
        if not year:
            raise WrongRequestException("Year not provided")

        try:
            model = CarModel.objects.get(modelName=modelName,year=year)
        except Exception as ex:
            raise WrongRequestException(str(ex))


        serializer.save(model=model,present=True)
    