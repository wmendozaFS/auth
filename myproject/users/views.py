from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LoginForm, RegisterForm

def home(request):
    return render(request, 'home.html')

def group_required(group_name):
    def decorator(view_func):
        @login_required
        @user_passes_test(lambda u: u.groups.filter(name=group_name).exists())
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@group_required('admin')
def admin_only_view(request):
    return render(request, 'users/admin_view.html')

@group_required('cliente')
def cliente_only_view(request):
    return render(request, 'users/cliente_view.html')

@group_required('staff')
def staff_only_view(request):
    return render(request, 'users/staff_view.html')

@group_required('premium')
def premium_only_view(request):
    return render(request, 'users/premium_view.html')

def user_login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    return render(request, 'users/login.html',{'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def register_user(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        group_name = request.POST['group']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email= request.POST['email']
        user = User.objects.create_user(username=username, password=password)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        return redirect('home')
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


def error_403(request, exception):
    return render(request, '403.html', status=403)
