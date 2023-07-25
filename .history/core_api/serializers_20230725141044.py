from rest_framework import serializers
from ..core.models import Empregador

class EmpregadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empregador
        fields = '__all__'