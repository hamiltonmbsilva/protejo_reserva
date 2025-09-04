from django.contrib import admin
from .models import Hotel, Quarto, Cliente, Reserva

# Cria uma classe Inline para gerenciar os Quartos diretamente no painel do Hotel
class QuartoInline(admin.TabularInline):
    model = Quarto
    extra = 1 # Adiciona um campo extra para adicionar novos quartos

# Customiza o painel de administração para o modelo Hotel
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'estado')
    search_fields = ('nome', 'cidade')
    inlines = [QuartoInline]

# Customiza o painel de administração para o modelo Quarto
@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'hotel', 'tipo', 'capacidade', 'preco_por_noite', 'disponivel')
    list_filter = ('hotel', 'tipo', 'disponivel')
    search_fields = ('numero', 'hotel__nome')

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