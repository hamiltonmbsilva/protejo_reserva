from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Hotel, Quarto, Cliente, Reserva, Proprietario
from .serializers import HotelSerializer, QuartoSerializer, ClienteSerializer, ReservaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum

def dashboard_view(request):
    # Dicionário para armazenar as métricas
    context = {}

    # Se o usuário for um superusuário, mostra todos os dados
    if request.user.is_superuser:
        hoteis = Hotel.objects.all()
    else:
        # Se não for superusuário, tenta encontrar o perfil de proprietário
        try:
            proprietario = Proprietario.objects.get(usuario=request.user)
            # Filtra os hotéis pelos que pertencem ao proprietário logado
            hoteis = Hotel.objects.filter(proprietario=proprietario)
        except Proprietario.DoesNotExist:
            # Se o usuário não for um proprietário, não mostra nada
            hoteis = Hotel.objects.none()

    # Cálculo das métricas para os hotéis filtrados
    total_hoteis = hoteis.count()
    
    # Obtém todos os quartos dos hotéis filtrados
    quartos = Quarto.objects.filter(hotel__in=hoteis)

    total_quartos = quartos.count()
    quartos_disponiveis = quartos.filter(disponivel=True).count()
    quartos_reservados = quartos.filter(disponivel=False).count()
    
    # Adiciona as métricas ao dicionário de contexto
    context = {
        'total_hoteis': total_hoteis,
        'total_quartos': total_quartos,
        'quartos_disponiveis': quartos_disponiveis,
        'quartos_reservados': quartos_reservados,
    }

    return render(request, 'dashboard.html', context)

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
