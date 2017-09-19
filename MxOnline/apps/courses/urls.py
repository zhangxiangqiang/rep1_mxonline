# _*_ coding:utf-8 _*_
from django.conf.urls import url, include
from courses.views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentsView, AddCommentsView, \
    VideoPlayView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
#     课程评论
    url(r'^comments/(?P<course_id>\d+)/$', CourseCommentsView.as_view(), name="course_comments"),

#     添加课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name="add_comment"),

#     视频播放
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play"),

]