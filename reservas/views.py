from django.shortcuts import render
from rest_framework import viewsets
from .models import Hotel, Quarto, Cliente, Reserva
from .serializers import HotelSerializer, QuartoSerializer, ClienteSerializer, ReservaSerializer
from django_filters.rest_framework import DjangoFilterBackend

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class QuartoViewSet(viewsets.ModelViewSet):
    queryset = Quarto.objects.all()
    serializer_class = QuartoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hotel'] # Permite filtrar quartos por id do hotel

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
