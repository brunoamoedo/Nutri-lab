from .utils import password_is_valid,email_html
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
import os
from django.conf import settings
from .models import Ativacao
from hashlib import sha256
# Create your views here.
def cadastro(request):
    if request.method == "GET":
        return render(request,'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirmar-senha')
        if not password_is_valid(request,senha,confirma_senha):
            return redirect('/auth/cadastro')
        try:
            user = User.objects.create_user(username=nome,
            email=email,
            password=senha,
            is_active=False)
            user.save()
            token = sha256(f"{nome}{email}".encode()).hexdigest()
            ativacao = Ativacao(token=token,user=user)
            ativacao.save()
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
            email_html(path_template, 'Cadastro confirmado', [email,], username=nome, link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}")
            messages.add_message(request,constants.SUCCESS,'Usuario cadastro com sucesso!')
            return redirect('/auth/login')
        except Exception:
           
            messages.add_message(request,constants.ERROR,'Erro interno do sistema')
            return redirect('/auth/cadastro')

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('login')
        senha = request.POST.get('senha')
        usuario = auth.authenticate(username=username, password=senha)
        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username ou senha invalidos')
            return redirect('/auth/login')
        else:
            auth.login(request, usuario)
            return redirect('/')
def sair(request):
    auth.logout(request)
    return redirect('/auth/login')
def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Essa token ja foi usado')
        return redirect('/auth/login')
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/login')
