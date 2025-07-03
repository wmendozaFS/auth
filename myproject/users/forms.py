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

class UserEditForm(forms.ModelForm):
    # Campos que quieres editar. ModelForm mapea automáticamente
    # los campos del modelo, pero puedes personalizarlos.

    # Aquí sobrescribimos first_name y last_name para que los labels sean "Nombre" y "Apellido"
    first_name = forms.CharField(max_length=150,
                                 label='Nombre',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}))
    last_name = forms.CharField(max_length=150,
                                label='Apellido',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el apellido'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el email'}),
                             validators=[email_validator])
    # Opcional: Si quieres permitir cambiar el grupo, añádelo aquí
    group = forms.ChoiceField(label='Rol',
                              choices=[(g.name, g.name.capitalize()) for g in Group.objects.all()],
                              widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'group'] # is_active es útil para activar/desactivar usuarios

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el formulario se inicializa con una instancia de usuario,
        # precarga el grupo actual del usuario.
        if self.instance and self.instance.pk:
            current_group = self.instance.groups.first()
            if current_group:
                self.fields['group'].initial = current_group.name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Si el usuario es el mismo que estamos editando, no validamos si ya existe.
        # Si cambiamos el username, sí debemos validar que el nuevo no exista.
        if self.instance and self.instance.username == username:
            return username
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        group_name = self.cleaned_data.get('group')

        if group_name:
            # Eliminar todos los grupos actuales del usuario y añadir el nuevo
            user.groups.clear()
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

        if commit:
            user.save()
        return user