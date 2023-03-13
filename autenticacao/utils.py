import re
from django.contrib import messages
from django.contrib.messages import constants


def password_is_valid(request, password, confirm_password):
    if len(password) < 6:
        messages.error(request, 'Sua senha deve conter 6 ou mais caracteres')
        return False

    if password != confirm_password:
        messages.error(request, 'As senhas nao coincidem!')
        return False

    if not re.search('[A-Z]', password):
        messages.error(request, 'Sua senha nao contem letras maiusculas')
        return False

    if not re.search('[a-z]', password):
        messages.error(request, 'Sua senha nao contem letras minusculas')
        return False

    if not re.search('[0-9]', password):
        messages.error(request, 'Sua senha nao contem numeros')
        return False

    return True