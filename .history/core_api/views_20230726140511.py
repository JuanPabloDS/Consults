from rest_framework import viewsets
from rest_framework import generics
from .models import Empregador
from .serializers import EmpregadorSerializer

class EmpregadorViewSet(generics.ListCreateAPIView):
    queryset = Empregador.objects.all()
    serializer_class = EmpregadorSerializer
