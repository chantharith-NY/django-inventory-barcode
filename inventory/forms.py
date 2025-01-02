from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, label="Email")
    password = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput)