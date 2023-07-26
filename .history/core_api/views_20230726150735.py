from rest_framework import viewsets, mixins
from .models import Empregador
from .serializers import EmpregadorSerializer

class EmpregadorViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Empregador.objects.all()
    serializer_class = EmpregadorSerializer
