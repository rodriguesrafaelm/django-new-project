from django.shortcuts import redirect, render
from django.contrib.auth.models import User
# Create your views here.


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if not nome.strip():
            print('O nome não pode ficar vazio')
            return redirect('cadastro')
        if not email.strip():
            print('O campo e-mail não pode ficar vazio')
            return redirect('cadastro')
        if senha != senha2:
            print('As senhas precisam ser iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            print('Usuário já cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        redirect('login')
        print('Cadastrado com sucesso')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    if request.method == 'POST':
       email = request.POST['email']
       senha = request.POST['senha']
       if email == '' or senha == '':
           print('Os campos e-mali e senha não podem ficar em branco.')
           return redirect('login')
       return redirect('dashboard')
    return render(request, 'usuarios/login.html')


def logout(request):
    pass

def dashboard(request):
    return render(request, 'usuarios/dashboard.html')