from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Hotel, Quarto, Cliente, Reserva, Proprietario
from .serializers import HotelSerializer, QuartoSerializer, ClienteSerializer, ReservaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.contrib.admin.models import LogEntry
from django.contrib.admin import site as admin_site 
from django.contrib import admin
from django.contrib.auth.models import AnonymousUser

def dashboard_view(request):
    context = {}

    original_context = admin_site.index(request).context_data

    if request.user.is_superuser:
        hoteis = Hotel.objects.all()
        total_clientes = Cliente.objects.count()
        total_reservas = Reserva.objects.count()
    else:
        try:
            proprietario = Proprietario.objects.get(usuario=request.user)
            hoteis = Hotel.objects.filter(proprietario=proprietario)
            total_clientes = 0
            total_reservas = 0
        except Proprietario.DoesNotExist:
            hoteis = Hotel.objects.none()
            total_clientes = 0
            total_reservas = 0

    total_hoteis = hoteis.count()    
    quartos = Quarto.objects.filter(hotel__in=hoteis)
    total_quartos = quartos.count()
    quartos_disponiveis = quartos.filter(disponivel=True).count()  
    total_clientes = Cliente.objects.count()
    total_reservas = Reserva.objects.count()
    quartos_alugados = total_quartos - quartos_disponiveis

    context = {
        'total_hoteis': total_hoteis,
        'total_quartos': total_quartos,
        'quartos_disponiveis': quartos_disponiveis,
        'quartos_alugados': quartos_alugados, # Variável corrigida
        'total_clientes': total_clientes,
        'total_reservas': total_reservas,        
    }

     # ADICIONE ESTA LINHA:
    print("Contexto enviado para o template:", original_context)

    return render(request, 'admin/index.html', original_context)

class HotelViewSet(viewsets.ModelViewSet):
    # O queryset é definido dinamicamente no get_queryset, então podemos deixá-lo comentado.
    # queryset = Hotel.objects.all() 
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Este método filtra a lista de hotéis por proprietário
    def get_queryset(self):
        # Passo 1: Se o usuário for um superusuário ou staff, mostre todos os hotéis
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Hotel.objects.all()
        
        # Passo 2: Se o usuário for anônimo (não logado), mostre todos os hotéis também.
        # Isso garante que a página inicial do front-end funcione para visitantes.
        if isinstance(self.request.user, AnonymousUser):
            return Hotel.objects.all()

        # Passo 3: Para um usuário autenticado que não é superusuário/staff,
        # filtre os hotéis pelo proprietário associado a ele.
        try:
            proprietario = Proprietario.objects.get(usuario=self.request.user)
            return Hotel.objects.filter(proprietario=proprietario)
        except Proprietario.DoesNotExist:
            # Se o usuário logado não tiver um Proprietario associado, não mostre hotéis.
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
        # Passo 1: Se o usuário for um superusuário ou staff, mostre todos os quartos.
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Quarto.objects.all()

        # Passo 2: Se o usuário for anônimo (não logado), mostre todos os quartos.
        # Isso é crucial para que o front-end de visitantes possa ver os quartos.
        if isinstance(self.request.user, AnonymousUser):
            return Quarto.objects.all()

        # Passo 3: Para um usuário comum autenticado, filtre pelos quartos do seu hotel.
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
