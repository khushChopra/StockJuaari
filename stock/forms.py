from django import forms
from .models import profile
from django.forms import ModelForm

'''
class NameForm(forms.ModelForm):
    class Meta:
        model = testmodel
        fields = ('name','age','date_of_birth')
'''

class ProfileForm(forms.Form):
    name= forms.CharField(max_length=50)
    email_ID= forms.CharField(max_length=50)
    password= forms.CharField(min_length=8, widget=forms.PasswordInput)
    confirm_password= forms.CharField(min_length=8, widget=forms.PasswordInput)
    company = forms.CharField(max_length=80)

class LoginForm(forms.Form):
    email_id= forms.CharField(max_length=50)
    password= forms.CharField(min_length=8, widget=forms.PasswordInput)

class FeedbackForm(forms.Form):
    name= forms.CharField(max_length=50)
    content= forms.CharField(max_length=1000)


class poForm(forms.Form):
    age= forms.IntegerField()
    company= forms.CharField(max_length=50)

class upform(ModelForm):
    class Meta:
        model = profile
        fields = ['name', 'photo', 'age', 'company', 'email', 'stocks']