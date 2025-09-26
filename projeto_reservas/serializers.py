# reservas/serializers.py
from rest_framework import serializers
from .models import Hotel, Quarto, Cliente, Reserva

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class QuartoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarto
        fields = '__all__'
        
# Você pode criar serializers para Cliente e Reserva também, se precisar