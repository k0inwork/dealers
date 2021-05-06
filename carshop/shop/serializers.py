from rest_framework import  serializers
from .models import Deal,Car

class DealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal
        fields = '__all__'
        depth = 1

class CarSerializer(serializers.ModelSerializer):


    class Meta:
        model = Car
        fields = '__all__'
        depth = 2
        read_only_fields = (['present'])