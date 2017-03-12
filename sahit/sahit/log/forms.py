from django.contrib.auth.forms import AuthenticationForm, User
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "receiver",
            "company",
            "hostelname",
            "room",
            "item",
        ]