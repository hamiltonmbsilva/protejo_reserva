# reservas/management/commands/setup_proprietario_group.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from reservas.models import Hotel, Quarto

class Command(BaseCommand):
    help = 'Cria o grupo "Proprietários" e atribui as permissões necessárias.'

    def handle(self, *args, **options):
        # 1. Cria ou obtém o grupo "Proprietários"
        proprietarios_group, created = Group.objects.get_or_create(name='Proprietários')

        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "Proprietários" criado com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Grupo "Proprietários" já existe. Atribuindo permissões...'))

        # 2. Obtém as permissões que criamos nos modelos
        content_type_hotel = ContentType.objects.get_for_model(Hotel)
        content_type_quarto = ContentType.objects.get_for_model(Quarto)

        permissoes_para_atribuir = [
            # Permissões do Django padrão (adicionar, editar, deletar)
            'add_hotel', 'change_hotel', 'delete_hotel', 'view_hotel',
            'add_quarto', 'change_quarto', 'delete_quarto', 'view_quarto',
            'add_reserva', 'change_reserva', 'view_reserva', # Reservas
            'add_cliente', 'change_cliente', 'view_cliente', # Clientes

            # Nossas permissões personalizadas
            'pode_gerenciar_hoteis',
            'pode_ver_metricas_proprietario',
            'pode_gerenciar_quartos',
            'pode_controlar_vagas',
        ]

        # 3. Adiciona as permissões ao grupo
        for codename in permissoes_para_atribuir:
            try:
                # Tenta encontrar a permissão usando o codename e o tipo de conteúdo
                if codename.endswith('_hotel') or codename == 'pode_gerenciar_hoteis' or codename == 'pode_ver_metricas_proprietario':
                    permissao = Permission.objects.get(codename=codename, content_type=content_type_hotel)
                elif codename.endswith('_quarto') or codename == 'pode_gerenciar_quartos' or codename == 'pode_controlar_vagas':
                    permissao = Permission.objects.get(codename=codename, content_type=content_type_quarto)
                else: # Outras permissões (clientes, reservas)
                    permissao = Permission.objects.get(codename=codename)
                
                proprietarios_group.permissions.add(permissao)
                self.stdout.write(self.style.SUCCESS(f'Permissão "{permissao}" adicionada.'))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permissão "{codename}" não encontrada. Verifique os nomes.'))

        self.stdout.write(self.style.SUCCESS('Configuração do grupo "Proprietários" finalizada.'))