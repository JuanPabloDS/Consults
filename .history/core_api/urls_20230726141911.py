from django.urls import path, include

from rest_framework.routers import SimpleRouter  #


from .views import (
    EmpregadorAPIView
    )


router = SimpleRouter()
router.register('empregador', EmpregadorAPIView)  # Registrando a rodo de cursos da API V2




urlpatterns = [
    path('empregador/', include(router.urls)),

]
