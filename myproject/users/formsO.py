from django import forms
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator

password_validator = RegexValidator(
    regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_\-])[A-Za-z\d@$!%*?&_\-]{6,}$',
    message="La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial."
)

email_validator = RegexValidator(
    regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
    message="Ingrese un correo electrónico válido."
)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, 
                               label='Usuario', 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su usuario'}))
    password = forms.CharField(label='Contraseña', 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}))

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, 
                               label='Usuario', 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su usuario'}))
    password = forms.CharField(label='Contraseña', 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}), 
                               validators=[password_validator])
    group = forms.ChoiceField(label='Rol', 
                              choices=[(g.name, g.name.capitalize()) for g in Group.objects.all()], 
                              widget=forms.Select(attrs={'class': 'form-select'}))
    first_name = forms.CharField(max_length=30, 
                             label='Nombre',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}))
    last_name = forms.CharField(max_length=30, 
                               label='Apellido', 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido'}))
    email = forms.EmailField(label='Email', 
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su email'}), 
                             validators=[email_validator])

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")
        return username