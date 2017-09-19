# _*_ coding:utf-8 _*_
from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, \
    AddFvaView, TeacherListView, TeacherDetailView

__author__ = 'qing'
__date__ = '2017/8/7 11:43'
from django.conf.urls import url, include

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<course_org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<course_org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<course_org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^org_teacher/(?P<course_org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
#     收藏与取消
    url(r'^add_fav/$', AddFvaView.as_view(), name="add_fav"),

#     讲师列表页
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),



]