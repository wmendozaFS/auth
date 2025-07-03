from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LoginForm, RegisterForm, UserEditForm # ¡Importa UserEditForm!

def home(request):
    return render(request, 'home.html')

# --- Decorador de grupo reutilizable ---
def group_required(group_name):
    def decorator(view_func):
        @login_required
        @user_passes_test(lambda u: u.groups.filter(name=group_name).exists())
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# --- Vistas protegidas por grupo ---
@group_required('admin') # Asumo que tu grupo de administradores se llama 'admin'
def admin_only_view(request):
    return render(request, 'users/editar_user.html')

@group_required('cliente')
def cliente_only_view(request):
    return render(request, 'users/cliente_view.html')

@group_required('staff')
def staff_only_view(request):
    return render(request, 'users/staff_view.html')

@group_required('premium')
def premium_only_view(request):
    return render(request, 'users/premium_view.html')

# --- Vistas de Autenticación ---
def user_login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username'] # Usar cleaned_data
        password = form.cleaned_data['password'] # Usar cleaned_data
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!') # Mensaje de éxito
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    return render(request, 'users/login.html',{'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.") # Mensaje informativo
    return redirect('login')

def register_user(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username'] # Usar cleaned_data
        password = form.cleaned_data['password'] # Usar cleaned_data
        group_name = form.cleaned_data['group'] # Usar cleaned_data
        first_name = form.cleaned_data['nombre'] # Corregido: usa 'nombre' de tu form a 'first_name' de User
        last_name = form.cleaned_data['apellido'] # Corregido: usa 'apellido' de tu form a 'last_name' de User
        email = form.cleaned_data['email'] # Usar cleaned_data

        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = first_name # Asignar explícitamente
        user.last_name = last_name # Asignar explícitamente
        user.save() # Guardar los cambios de first_name y last_name

        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        messages.success(request, "¡Registro exitoso! Ya puedes iniciar sesión.")
        return redirect('login') # Redirigir a login después del registro exitoso
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')

# --- Vistas para Edición de Usuarios (Nuevas) ---
def is_admin_or_superuser(user):
    # Asegúrate de que el grupo 'admin' exista o cámbialo por el nombre de tu grupo de administradores
    return user.is_superuser or user.groups.filter(name='admin').exists()

@login_required
@user_passes_test(is_admin_or_superuser, login_url='users/login.html') # Redirige si no tiene permiso
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user) # Importante: pasar la instancia del usuario
        if form.is_valid():
            form.save()
            messages.success(request, f'El usuario "{user.username}" ha sido actualizado correctamente.')
            return redirect('user_list') # Redirige a una lista de usuarios, por ejemplo
    else:
        form = UserEditForm(instance=user) # Pre-rellena el formulario con los datos del usuario
    return render(request, 'users/editar_user.html', {'form': form, 'user_to_edit': user})

@login_required
@user_passes_test(is_admin_or_superuser, login_url='users/login.html')
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'users/user_list.html', {'users': users})

# --- Vistas de Errores ---
def error_403(request, exception):
    return render(request, '403.html', status=403)

# Opcional: una vista para la página prohibida si `user_passes_test` redirige allí
def forbidden_access(request):
    return render(request, 'users/login.html') # Asegúrate de tener este template