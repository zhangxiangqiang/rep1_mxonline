# _*_ coding:utf-8 _*_
from django.conf.urls import url, include

from users.views import UsercenterInfoView, ImageUploadView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, \
    MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    url(r'^usercenter_info/$', UsercenterInfoView.as_view(), name="usercenter_info"),
    url(r'^image/upload/$', ImageUploadView.as_view(), name="image_upload"),

   #  个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    #  发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
   #  修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
   #  我的收藏
    url(r'^myfav/orgs/$', MyFavOrgView.as_view(), name="myfav_org"),
    url(r'^myfav/teachers/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    url(r'^myfav/courses/$', MyFavCourseView.as_view(), name="myfav_course"),

    # 我的消息
    url(r'^mymessages/$', MyMessageView.as_view(), name="mymessages"),

   ]