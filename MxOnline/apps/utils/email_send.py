# _*_ coding:utf-8 _*_
from random import Random
from django.core.mail import send_mail

from MxOnline.settings import EMAIL_FROM
from users.models import EmailVerifyRecord

__author__ = 'qing'
__date__ = '2017/8/1 18:39'


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_title = ""
    email_body = ""
    email_record.save()
    if send_type == "register":
        email_title = "学而强激活"
        email_body = "请点击下面链接完成注册:http://127.0.0.1:8000/active/{0}".format(code)
    elif send_type == "forget":
        email_title = "重置密码"
        email_body = "请点击下面链接重新设置密码:http://127.0.0.1:8000/reset/{0}".format(code)
    elif send_type == "update_email":
        email_title = "学而强修改邮箱验证码"
        email_body = "您的验证码是:{0}".format(code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass


