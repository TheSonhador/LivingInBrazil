from django.core.exceptions import ValidationError
import re
from django import forms


# def teste(value):
#     if value == 'oi':
#         raise ValidationError(f'deu ruim')
#     else:
#         pass

def telefone(value):
    padrao = '([0-9]{2,3})?([0-9]{2})([0-9]{4,5})([0-9]{4})'
    numero = str(value)
    teste = re.findall(padrao, numero)

    if not teste:
        raise ValidationError(f'O número {value} não é válido, por favor digite o codigo do pais, o dd, e 8 ou 9 numeros', params={'value':value})
    else:
        pass



















class telefoneForm(forms.Field):

    def validate(self, value):
        padrao = '([0-9]{2,3})?([0-9]{2})([0-9]{4,5})([0-9]{4})'
        numero = str(value)
        teste = re.findall(padrao, numero)

        if not teste:
            raise ValidationError(f'O número {value} não é válido, por favor digite o codigo do pais, o dd, e 8 ou 9 numeros', params={'value':value})
        else:
            pass