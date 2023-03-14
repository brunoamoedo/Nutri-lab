import re
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings



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
def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}
