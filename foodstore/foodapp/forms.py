# listings/forms.py

from django import forms

class LoginForm(forms.Form):
   username = forms.CharField(required=True)
   password = forms.CharField(max_length=100)
   
