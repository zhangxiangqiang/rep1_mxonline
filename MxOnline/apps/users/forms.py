# _*_ coding:utf-8 _*_
from django import forms
from captcha.fields import CaptchaField

from users.models import UserProfile

__author__ = 'qing'
__date__ = '2017/7/30 17:45'


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ResetForm(forms.Form):
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UsercenterInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'email']


