from django import forms
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator

password_validator = RegexValidator(
    regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_\-])[A-Za-z\d@$!%*?&_\-]{6,}$',
    message="La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial."
)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Usuario", widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    username = forms.CharField(
          max_length=150, 
          label="Usuario", 
          widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(
          label="Contraseña", 
          widget=forms.PasswordInput(attrs={'class': 'form-control'}),
          validators=[password_validator])
    group = forms.ChoiceField(
          choices=[(g.name, g.name.capitalize()) for g in Group.objects.all()], 
          label="Rol",
          widget=forms.Select(attrs={"class": "form-select"})
    )

     def clean_username(self):
       username = self.cleaned_data.get('username')
          if User.objects.filter(username=username).exists():
               raise forms.ValidationError("Este usuario ya existe")
          return username