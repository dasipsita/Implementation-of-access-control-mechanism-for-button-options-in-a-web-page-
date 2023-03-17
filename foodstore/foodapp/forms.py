# listings/forms.py

from django import forms

class show_access_form(forms.Form):
   userID = forms.CharField(required=True)
   formID = forms.CharField(widget=forms.HiddenInput(), initial="show_access_form") 
class add_access_form(forms.Form):
   userID = forms.CharField(required=True)
   MenuID = forms.CharField(max_length=100)
   formID = forms.CharField(widget=forms.HiddenInput(), initial="add_access_form") 
class remove_access_form(forms.Form):
   userID = forms.CharField(required=True)
   MenuID = forms.CharField(max_length=100)
   formID = forms.CharField(widget=forms.HiddenInput(), initial="remove_access_form") 
class check_access_form(forms.Form):
   userID = forms.CharField(required=True)
   MenuID = forms.CharField(max_length=100)
   formID = forms.CharField(widget=forms.HiddenInput(), initial="check_access_form") 
class add_superuser_form(forms.Form):
   userID = forms.CharField(required=True)   
   formID = forms.CharField(widget=forms.HiddenInput(), initial="add_superuser_form") 
class remove_user_form(forms.Form):
   userID = forms.CharField(required=True)
   formID = forms.CharField(widget=forms.HiddenInput(), initial="remove_user_form")        
   
