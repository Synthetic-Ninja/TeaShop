from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'user-name',
        'placeholder': 'Username'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'name': 'user-password',
        'placeholder': 'Password'}))

    remember_me = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    action = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('username', 'passwords')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'user-name',
        'placeholder': 'Username'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'name': 'user-password',
        'placeholder': 'Password'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'name': 'user-password2',
        'placeholder': 'Repeat password'}))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'name': 'user-email',
        'placeholder': 'Email'}))

    action = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
