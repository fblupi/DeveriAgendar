from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *


def index(request):  #
    return render(request, 'home.html')

def login(request):  #
    
    return render(request, 'login.html')

class SignUp(generic.CreateView):
    form_class = UserCreationForm #Aqui puxa um form padrão
    success_url = reverse_lazy('login') #Redireciona para a pagina de login
    template_name = 'cadastro.html'

def cadastrar(request):  #
    return render(request, 'cadastro.html')

def lista_contas(request):  # metado de teste pego do SGE
    lista_tipos = Usuario.objects.all()
    return render(request, 'tipo.html', context={'tipos': lista_tipos})

def create_conta(request):  # metado de teste pego do SGE
    return render(request, 'pessoa_form.html', context=None)

# esse metado cria o usuario apartir de um formulario completo, ele não está completo e está apresentando erro.
# a cricação do usuario em si está funcionando, o erro está na criação do "Perfil"
# metados de teste pego do SGE.
# @transaction.atomic
def salvar_conta(request):  # primeira forma utilizando chave estrangeira

    login = request.POST.get('login')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    if login and senha:
        if senha == senha2:
            user = User()
            user.username = login
            user.password = senha
            user.save()  # aqui voce cria o usuario

            usuario2 = Usuario()  # Aqui voce instancia a class usuario
            usuario2.usuario = user  # class Usuario recebe a class User do django
            usuario2.save()  # salva a class Usuario

            nome = request.POST.get('nome')
            email = request.POST.get('email')
            email2 = request.POST.get('email')
        else:
            print("entrou else")
            messages.info(request,'Senha estão invalidas')
            return HttpResponseRedirect('/criarconta/')

        if nome and email:
            if email == email2:
                p = Pessoa()  # Inicia a class Pessoa
                usuario2.nome = nome  # Como atributo de nome estão na class Usuario quem recebe os atributos de nome e email e ela quem recebe
                usuario2.email = email
                usuario2.save()  # aqui voce cria a class
                p.pessoa = usuario2
                p.save()
            else:
                messages.info(request, 'Email errados')

                return HttpResponseRedirect('/criarconta/')

        return redirect('/contas')

#@login_required
def show_calendar(request):
    evento = CompromissoPessoal.objects.all()
    return render(request, 'calendar.html', context={'evento': evento})

#@login_required
def agendas_publicas(request,username):
    lista_agendas = AgendaPublica.objects.filter(AgendaPublica.dono == username)

    return render(request, 'agenda_publica.html', context={'nome': lista_agendas})

# @login_required
def agendas_privadas(request):
    agendas = AgendaPrivada.objects.all()

    return render(request, 'agenda_privada.html', context={'agenda_privada': agendas})

#@login_required
def create_compromissoPessoal(request):
    titulo = request.POST.get(' tituloEvent ')
    descricao = request.POST.get(' descricaoEvent ')
    local = request.POST.get(' localEvent ')
    dt_inicio = request.POST.get(' dtBeginEvent ')
    hr_inicio = request.POST.get(' hourBeginEvent ')
    dt_fim = request.POST.get(' dtEndEvent ')
    hr_fim = request.POST.get(' hourEndEvent ')
    compromisso = request.POST.get(' Compromisso ')
    foto = request.POST.get(' InputFile ')

    evento = CompromissoPessoal()

    if titulo:
        evento.titulo = titulo

        if descricao:
            evento.discricao = descricao

        if local:
            evento.local = local

        if dt_inicio:
            evento.dataInicio = dt_inicio

        if hr_inicio:
            evento.horaInicio = hr_inicio

        if dt_fim:
            evento.dataFim = dt_fim

        if hr_fim:
            evento.horaFim = hr_fim

        if compromisso:
            evento.compromisso = compromisso

        if foto:
            evento.foto = foto

        evento.save()

        return render(request,'calendar.html',context=None)
    else:
        return redirect('/createEventoPessoal/')

#@login_required
def create_agendaPublica(request):
    form = AgendaPublicaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('agendaspublicas')
    return render(request, 'agenda_publica_form.html', context={'form': form})

#@login_required
def update_agendaPublica(request, pk):
    ag = AgendaPublica.objects.get(pk=pk)

    form = AgendaPublicaForm(request.POST or None, instance=agendas_publicas)
    if form.is_valid():
        form.save()
        return redirect('createagendapublica/')
    return render(request, 'agenda_publica_form.html', {'object': ag, 'form': form})

#@login_required
def create_agendaPrivada(request):
    form = AgendaPrivadaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('agendasprivadas')
    return render(request, 'agenda_privada_form.html', context={'form': form})


