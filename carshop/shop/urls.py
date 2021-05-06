from django.urls import path
from .views import ViewDeals, SellCarView, ViewAvailableCars, CreateCar

urlpatterns = [
     path('deals', ViewDeals.as_view()),
     path('sell', SellCarView.as_view()),
     path('cars', ViewAvailableCars.as_view()),
     path('addCar', CreateCar.as_view())
 ]