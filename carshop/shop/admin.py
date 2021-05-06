from django.contrib import admin
from .models import CarModel, Dealer, Car, Manufactorer, Deal
from django.contrib.auth.models import User

admin.site.register(Dealer)

class ManAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Manufactorer,ManAdmin)

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['modelName','manufactorer','year']
admin.site.register(CarModel,CarModelAdmin)

class CarAdmin(admin.ModelAdmin):
    list_display = ['model','price','present','vin']
admin.site.register(Car,CarAdmin)

class DealAdmin(admin.ModelAdmin):
    def carprice(obj):
        return obj.car.price
    list_display = ['dealer','car',carprice,'realprice']
admin.site.register(Deal,DealAdmin)
