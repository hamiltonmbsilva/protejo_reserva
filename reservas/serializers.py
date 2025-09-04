from rest_framework import serializers
from .models import Hotel, Quarto, Cliente, Reserva

# Serializer para o modelo Quarto
class QuartoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarto
        fields = '__all__' # Inclui todos os campos do modelo Quarto

# Serializer para o modelo Hotel
# Adicionamos 'quartos' como um campo aninhado para mostrar todos os quartos de um hotel
class HotelSerializer(serializers.ModelSerializer):
    quartos = QuartoSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'nome', 'descricao', 'endereco', 'cidade', 'estado', 'pais','imagem_principal', 'quartos']

# Serializer para o modelo Cliente
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

# Serializer para o modelo Reserva
class ReservaSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField(read_only=True)
    quarto = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reserva
        fields = ['id', 'cliente', 'quarto', 'data_check_in', 'data_check_out', 'status', 'data_criacao']