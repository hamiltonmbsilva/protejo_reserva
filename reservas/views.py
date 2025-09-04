from django.shortcuts import render
from rest_framework import viewsets
from .models import Hotel, Quarto, Cliente, Reserva
from .serializers import HotelSerializer, QuartoSerializer, ClienteSerializer, ReservaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum

# View para o Dashboard Administrativo
def dashboard_view(request):
    # Obtendo as métricas do banco de dados
    total_hoteis = Hotel.objects.count()
    total_quartos = Quarto.objects.count()
    
    # Para contar quartos alugados e disponíveis, precisamos de uma lógica mais avançada
    # Simplificando a lógica para contar reservas com status 'Reservado'
    quartos_alugados = Reserva.objects.filter(status='Reservado').count()
    quartos_disponiveis = total_quartos - quartos_alugados
    
    total_clientes = Cliente.objects.count()
    total_reservas = Reserva.objects.count()
    
    # Passando os dados para o template
    context = {
        'total_hoteis': total_hoteis,
        'total_quartos': total_quartos,
        'quartos_alugados': quartos_alugados,
        'quartos_disponiveis': quartos_disponiveis,
        'total_clientes': total_clientes,
        'total_reservas': total_reservas,
    }
    
    return render(request, 'admin/index.html', context)

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
