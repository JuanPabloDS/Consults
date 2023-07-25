from rest_framework import viewsets
from .models import Empregador
from .serializers import EmpregadorSerializer

class EmpregadorViewSet(viewsets.ModelViewSet):
    queryset = Empregador.objects.all()
    serializer_class = EmpregadorSerializer
