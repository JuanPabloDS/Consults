from django.test import TestCase

from itertools import cycle

contrato = 'Mensal'
error_message = 'Foi'

if contrato != 'Mensal':
    if contrato != 'Anual':
        error_message = 'O contrato não é válido'


elif len(contrato) > 10:
    error_message = 'O contrato não é váaaalido'


print(error_message)