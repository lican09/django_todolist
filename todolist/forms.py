﻿#-*- coding:utf-8-*-
from django import forms


class LoginForm(forms.Form):
    '''
    LoginForm
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})

class RegForm(forms.Form):
    '''
    RegForm
    '''
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
                              max_length=50,error_messages={"required": "email不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})


class EditPassForm(forms.Form):
    '''
    EditForm
    '''
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "输入密码", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "再次输入", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})