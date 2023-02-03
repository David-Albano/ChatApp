from django.forms import ModelForm, EmailInput, PasswordInput
from django import forms
from chat.models import ChatUsers

class UserFormLogin(ModelForm):
    class Meta:
        model = ChatUsers
        fields = ['email', 'password']
        widgets = {
            'email': EmailInput(attrs={'type': 'email'}),
            'password': PasswordInput(attrs={'type': 'password'})
        }

class UserFormSignin(ModelForm):
    class Meta:
        model = ChatUsers
        fields = ['username', 'email', 'password']
        widgets = {
            'email': EmailInput(attrs={'type': 'email'}),
            'password': PasswordInput(attrs={'type': 'password'})
        }

class AddContactForm(forms.Form):
    contact1 = forms.CharField(
        label='Contact Nº1',
        widget=forms.TextInput(attrs={'readonly': True}),
        max_length=255)
    contact2 = forms.CharField(
        label='Contact Nº1',
        widget=forms.TextInput(attrs={'placeholder': 'Enter the username you wanna add'}),
        max_length=255)
