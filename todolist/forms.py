#-*- coding:utf-8-*-
from django import forms


class LoginForm(forms.Form):
    '''
    ��¼Form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username����Ϊ��",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password����Ϊ��",})

class RegForm(forms.Form):
    '''
    ע���
    '''
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
                              max_length=50,error_messages={"required": "email����Ϊ��",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password����Ϊ��",})
