from django.urls import path

from rest_framework.routers import SimpleRouter  #


from .views import (
    EmpregadorViewSet
    )


router = SimpleRouter()
router.register('empregador', EmpregadorViewSet)  # Registrando a rodo de cursos da API V2




urlpatterns = [
    path('empregador/', EmpregadorViewSet.as_view(), name='empregador'),

]
