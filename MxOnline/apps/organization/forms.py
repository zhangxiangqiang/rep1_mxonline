# _*_ coding:utf-8 _*_
from operation.models import UserAsk
import re
from django import forms
__author__ = 'qing'
__date__ = '2017/8/7 12:01'


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^17\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号非法", code="mobile_invalid")


