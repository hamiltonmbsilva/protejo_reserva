from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, QuartoViewSet, ClienteViewSet, ReservaViewSet

router = DefaultRouter()
router.register(r'hoteis', HotelViewSet, basename='hoteis')
router.register(r'quartos', QuartoViewSet, basename='quartos')
router.register(r'clientes', ClienteViewSet)
router.register(r'reservas', ReservaViewSet)

# As URLs geradas pelo router são incluídas na lista abaixo
urlpatterns = router.urls