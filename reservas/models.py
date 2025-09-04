from django.db import models

# Modelo para o Hotel
class Hotel(models.Model):
    nome = models.CharField(max_length=200, help_text="Nome do hotel.")
    descricao = models.TextField(blank=True, help_text="Descrição detalhada do hotel.")
    endereco = models.CharField(max_length=255, help_text="Endereço completo do hotel.")
    cidade = models.CharField(max_length=100, help_text="Cidade onde o hotel está localizado.")
    estado = models.CharField(max_length=100, help_text="Estado onde o hotel está localizado.")
    pais = models.CharField(max_length=100, help_text="País onde o hotel está localizado.")
    imagem_principal = models.ImageField(upload_to='hoteis_imagens/', blank=True, null=True, help_text="Imagem principal do hotel.")
    
    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotéis"
        
    def __str__(self):
        return self.nome

# Modelo para o Quarto
class Quarto(models.Model):
    TIPO_CHOICES = [
        ('solteiro', 'Solteiro'),
        ('casal', 'Casal'),
        ('suite', 'Suíte'),
        ('familia', 'Família'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='quartos', help_text="Hotel ao qual o quarto pertence.")
    numero = models.CharField(max_length=10, help_text="Número ou identificador do quarto.")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='casal', help_text="Tipo de quarto.")
    capacidade = models.IntegerField(help_text="Número máximo de hóspedes.")
    preco_por_noite = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço por noite.")
    disponivel = models.BooleanField(default=True, help_text="Status de disponibilidade.")
    imagem = models.ImageField(upload_to='quartos_imagens/', blank=True, null=True, help_text="Imagem do quarto.")
    
    class Meta:
        verbose_name = "Quarto"
        verbose_name_plural = "Quartos"
        unique_together = ('hotel', 'numero') # Garante que o número do quarto seja único por hotel

    def __str__(self):
        return f"Quarto {self.numero} ({self.hotel.nome})"

# Modelo para o Cliente
class Cliente(models.Model):
    nome = models.CharField(max_length=100, help_text="Nome completo do cliente.")
    email = models.EmailField(unique=True, help_text="Endereço de e-mail.")
    telefone = models.CharField(max_length=20, blank=True, help_text="Número de telefone.")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome

# Modelo para a Reserva
class Reserva(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('concluida', 'Concluída'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas', help_text="Cliente que fez a reserva.")
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='reservas', help_text="Quarto reservado.")
    data_check_in = models.DateField(help_text="Data de check-in.")
    data_check_out = models.DateField(help_text="Data de check-out.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', help_text="Status da reserva.")
    data_criacao = models.DateTimeField(auto_now_add=True, help_text="Data e hora da criação da reserva.")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Reserva de {self.cliente.nome} para o Quarto {self.quarto.numero}"
