"""
URL configuration for projeto_reservas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reservas.views import dashboard_view
from django.conf import settings # Importe as configurações
from django.conf.urls.static import static # Importe a função para servir arquivos estáticos
# Importe a sua nova instância do painel de administração
from reservas.admin import proprietario_admin_site
from rest_framework.routers import DefaultRouter
from reservas.views import HotelViewSet, QuartoViewSet # Importe QuartoViewSet


# Atribua a dashboard_view à instância de admin que será usada
proprietario_admin_site.index = dashboard_view

# Configure o template que a view irá usar
proprietario_admin_site.index_template = 'index.html'

router = DefaultRouter()
router.register(r'hoteis', HotelViewSet, basename='hoteis')
router.register(r'quartos', QuartoViewSet, basename='quartos') # Adicione a rota para quartos

urlpatterns = [    
    path('admin/', proprietario_admin_site.urls),
    path('api/', include('reservas.urls')),
    path('api/', include(router.urls)),
]


#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Sobrescreve a página inicial do admin para usar nossa view
#admin.site.index = dashboard_view

# Adiciona a URL de mídia apenas em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
