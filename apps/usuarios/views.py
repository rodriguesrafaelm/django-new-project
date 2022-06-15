from email import message
from unicodedata import name
from urllib import response
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita
# Create your views here.


def cadastro(request):
    """Cadastra uma nova pessoa no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha1 = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O nome não pode ficar vazio')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'O campo e-mail não pode ficar vazio')
            return redirect('cadastro')
        if comparar_igualdade_senhas(senha1, senha2):
            messages.error(request, 'As senhas não são iguais')
            print('As senhas precisam ser iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=name).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha1)
        user.save()
        redirect('login')
        print('Cadastrado com sucesso')
        messages.success(request, 'Cadastrado com sucesso')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    """Realiza o log-in de uma pessoa no sistema"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            print('Os campos e-mali e senha não podem ficar em branco.')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True)
            user = auth.authenticate(request, username=nome[0], password=senha)
            print(user)
            if user is not None:
                auth.login(request, user)
                print('Logado com sucesso')
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')


def logout(request):
    """Deslogar o cliente"""
    auth.logout(request)
    return(redirect('index'))

def dashboard(request):
    """Exibir a dashboard caso o usuário esteja autenticado"""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)
        
        dados={
            'receitas': receitas
        }
        
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def campo_vazio(campo):
    """Verifica se o valor é vazio"""
    return not campo.strip()

def comparar_igualdade_senhas(senha1, senha2):
    """Compara os valores dos campos de senha no cadastro"""
    return senha1 != senha2