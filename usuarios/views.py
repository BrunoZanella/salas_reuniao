from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UsuarioForm, UsuarioUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout

def cadastro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

@login_required
def perfil(request):
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = UsuarioUpdateForm(instance=request.user)
    return render(request, 'usuarios/perfil.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Você saiu com sucesso!')
    return redirect('home')
