"""
Django web app to manage and store drillhole data.
Copyright (C) 2023 Jorge Fuertes Blanco

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from DH_app.models import General_DH, Projects, Images

username_validator = UnicodeUsernameValidator()

class CustomUserCreationForm(UserCreationForm):
    # Crear campos y especificar el tipo de datos.
    username = forms.CharField(max_length = 12, help_text= "Required. User Name", 
        validators=[username_validator], 
        error_messages={'unique': _("A user with that username already exist.")}, required= True, 
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    first_name = forms.CharField(max_length = 32, help_text= "Required. First Name",required= True, 
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))

    last_name = forms.CharField(max_length = 32, help_text= "Required. Last Name",required= True, 
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    email = forms.CharField(max_length = 32, help_text= "Insert a valid email address",
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))

    password1 = forms.CharField(label = _("Password"), 
        widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), 
        help_text= password_validation.password_validators_help_text_html())
        
    password2 = forms.CharField( label = _("Password confirmation"),
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}),
        help_text= _("Please insert the same password again."))
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

'''
Form para crear un nuevo proyecto
'''
class CreateProject(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ('__all__')


'''
Form para importar datos
''' 
class DataImportForm (forms.ModelForm):
    class Meta:
        model= General_DH
        fields = ('__all__')

'''
Form para seleccionar datos
'''
class SelectDataForm(forms.ModelForm):
    class Meta:
        model = General_DH
        fields = ('ID',)
'''
Form para actualizar datos
'''
class UpdateDataForm(forms.ModelForm):
    class Meta:
        model = General_DH
        fields = ('project', 'DH_id',)


'''
Form para borrar datos de sondeos
'''
class DeleteDataForm(forms.ModelForm):
    class Meta:
        model = General_DH
        fields = ('project', 'DH_id',)
'''
Form para cargar las imagenes
'''

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ("__all__")