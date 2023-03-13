from .utils import password_is_valid
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from time import sleep
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
            messages.add_message(request,constants.SUCCESS,'Usuario cadastro com sucesso!')
            sleep(3)
            return redirect('/auth/login')
        except Exception:
            messages.add_message(request,constants.ERROR,'Erro interno do sistema')
            return redirect('/auth/cadastro')

def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    elif request.method == "POST":
        return HttpResponse("Testando")