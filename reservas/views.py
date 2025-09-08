from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Hotel, Quarto, Cliente, Reserva, Proprietario
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
    #queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Este método filtra a lista de hotéis por proprietário
    def get_queryset(self):
        # Se o usuário for um superusuário ou staff, mostre todos os hotéis
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Hotel.objects.all()
        
        # Para um usuário comum, filtre por proprietário
        try:
            proprietario = Proprietario.objects.get(usuario=self.request.user)
            return Hotel.objects.filter(proprietario=proprietario)
        except Proprietario.DoesNotExist:
            return Hotel.objects.none()

    # Este método garante que um novo hotel seja automaticamente associado ao proprietário logado
    def perform_create(self, serializer):
        try:
            proprietario = Proprietario.objects.get(usuario=self.request.user)
            serializer.save(proprietario=proprietario)
        except Proprietario.DoesNotExist:
            # Você pode levantar um erro ou impedir a criação se o usuário não for um proprietário
            pass

class QuartoViewSet(viewsets.ModelViewSet):
    queryset = Quarto.objects.all()
    serializer_class = QuartoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hotel'] 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Este método filtra a lista de quartos pelos hotéis do proprietário logado
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Quarto.objects.all()

        try:
            proprietario = Proprietario.objects.get(usuario=self.request.user)
            # Filtra os quartos pelos hotéis que pertencem a este proprietário
            return Quarto.objects.filter(hotel__proprietario=proprietario)
        except Proprietario.DoesNotExist:
            return Quarto.objects.none()

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
