from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import  User,Group
from .models import Hotel, Quarto, Cliente, Reserva, Proprietario

# 1. Crie uma classe de AdminSite personalizada
class ProprietarioAdminSite(AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        # Se o usuário não for um superusuário, filtre a lista de apps
        if not request.user.is_superuser:
            # Lista de apps que o proprietário deve ver
            apps_permitidos = ['reservas']
            
            nova_app_list = []
            for app in app_list:
                # Mantenha apenas os apps permitidos
                if app['app_label'].lower() in apps_permitidos:
                    # Filtra os modelos dentro dos apps
                    modelos_permitidos = ['hotel', 'quarto', 'reserva', 'cliente']
                    
                    if app['app_label'].lower() == 'reservas':
                        app['models'] = [
                            m for m in app['models'] 
                            if m['object_name'].lower() in modelos_permitidos
                        ]
                    nova_app_list.append(app)
            return nova_app_list
        
        return app_list

# 2. Crie uma instância do seu painel personalizado
proprietario_admin_site = ProprietarioAdminSite(name='proprietario_admin')

# 3. Registre todos os modelos (padrão e personalizados) na nova instância
proprietario_admin_site.register(Proprietario)
proprietario_admin_site.register(Hotel)
proprietario_admin_site.register(Quarto)
proprietario_admin_site.register(Cliente)
proprietario_admin_site.register(Reserva)

# Registre os modelos padrão do Django
proprietario_admin_site.register(User)
proprietario_admin_site.register(Group)



# Registra o modelo Proprietario
@admin.register(Proprietario)
class ProprietarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefone', 'data_criacao')
    search_fields = ('usuario__username', 'telefone')


# Cria uma classe Inline para gerenciar os Quartos diretamente no painel do Hotel
class QuartoInline(admin.TabularInline):
    model = Quarto
    extra = 1 # Adiciona um campo extra para adicionar novos quartos

# Customiza o painel de administração para o modelo Hotel
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'estado', 'proprietario')
    list_filter = ('cidade', 'pais', 'proprietario')
    search_fields = ('nome', 'cidade', 'pais')
     # Este método filtra o queryset para mostrar apenas os hotéis do proprietário logado
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Se o usuário não for um superusuário, filtre por proprietário
        if not request.user.is_superuser:
            try:
                # Tenta encontrar o perfil de proprietário do usuário
                proprietario = Proprietario.objects.get(usuario=request.user)
                return queryset.filter(proprietario=proprietario)
            except Proprietario.DoesNotExist:
                # Se o usuário não tiver um perfil de proprietário, não mostre nada
                return queryset.none()
        return queryset

# Customiza o painel de administração para o modelo Quarto
@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'hotel', 'tipo', 'capacidade', 'preco_por_noite', 'disponivel')
    list_filter = ('hotel', 'tipo', 'disponivel')
    search_fields = ('numero', 'hotel__nome')
    # Este método filtra o queryset para mostrar apenas os quartos dos hotéis do proprietário logado
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Se o usuário não for um superusuário, filtre por proprietário
        if not request.user.is_superuser:
            try:
                proprietario = Proprietario.objects.get(usuario=request.user)
                # Filtra os quartos pelos hotéis que pertencem a este proprietário
                return queryset.filter(hotel__proprietario=proprietario)
            except Proprietario.DoesNotExist:
                return queryset.none()
        return queryset

# Cria uma classe Inline para gerenciar as Reservas de um Cliente
class ReservaInline(admin.TabularInline):
    model = Reserva
    extra = 0
    readonly_fields = ('quarto', 'data_check_in', 'data_check_out', 'status', 'data_criacao')
    can_delete = False

# Customiza o painel de administração para o modelo Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email')
    inlines = [ReservaInline]

# Customiza o painel de administração para o modelo Reserva
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'quarto', 'data_check_in', 'data_check_out', 'status')
    list_filter = ('status', 'data_check_in', 'data_check_out')
    search_fields = ('cliente__nome', 'quarto__numero')
    autocomplete_fields = ['cliente', 'quarto']