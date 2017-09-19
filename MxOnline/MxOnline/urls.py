# _*_ coding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve

import users
from MxOnline.settings import MEDIA_ROOT
import xadmin
from django.views.generic import TemplateView

from organization.views import OrgView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ModifyPwdView, ResetView, LogoutView, \
    IndexView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^index/$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forgetpwd/$', ForgetPwdView.as_view(), name="forgetpwd"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset"),
    url(r'^modify/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程相关
    url(r'^course/', include('courses.urls', namespace='course')),
    #   上传文件的访问处理
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
#     全局404和500处理
#     url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
# 用户相关
    url(r'^users/', include('users.urls', namespace='users')),
#     集成富文本
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'





