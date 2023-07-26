from rest_framework import generics
from .models import Empregador
from .serializers import EmpregadorSerializer

class EmpregadorAPIView(generics.ListCreateAPIView):
    queryset = Empregador.objects.all()
    serializer_class = EmpregadorSerializer

class EmpregadorEdtAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Empregador.objects.all()
    serializer_class = EmpregadorSerializer
