from django.contrib import admin
import datetime
from django.db import models
import django.utils

# Create your models here.

colorChoices = [
    ('Red','Red'),
    ('White','White'),
    ('Black','Black'),
    ('Blue','Blue'),
    ('Green','Green'),
    ('Grey','Grey')
]

yearChoices = [(r,r) for r in range(1984, datetime.date.today().year+1)]

class Manufactorer(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class CarModel(models.Model):
    manufactorer = models.ForeignKey('Manufactorer',on_delete=models.CASCADE)
    modelName = models.CharField(max_length=30)
    year = models.IntegerField('year', choices=yearChoices, default=datetime.datetime.now().year)
    def __str__(self):
        return str(self.manufactorer)+" "+self.modelName+" ("+str(self.year)+")"

class Car(models.Model):
    model = models.ForeignKey('CarModel',on_delete=models.CASCADE)
    color = models.CharField(choices = colorChoices, default='White',max_length=6)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    @property
    @admin.display(
        description='Vehicle VIN',
    )  
    def vin(self):
        return self.serialid

    serialid = models.IntegerField() #vin
    present = models.BooleanField()

    def __str__(self):
        return self.color +" "+str(self.model)

class Dealer(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    def __str__(self):
        return self.name


class Deal(models.Model):

    car = models.ForeignKey('Car',on_delete=models.CASCADE)
    dealer = models.ForeignKey('Dealer',on_delete=models.CASCADE)
    realprice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null = True)
    date = models.DateTimeField(default=django.utils.timezone.now)