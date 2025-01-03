from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput)