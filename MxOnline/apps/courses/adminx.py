# _*_ coding:utf-8 _*_
import xadmin
__author__ = 'qing'
__date__ = '2017/7/27 8:50'

from .models import Course, Lesson, Video, CourseResourse, BannerCourse


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'click_nums', 'fav_nums', 'image',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'click_nums', 'fav_nums', 'image']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'click_nums', 'fav_nums', 'image',
                   'add_time']

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'click_nums', 'fav_nums', 'image',
                    'add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'click_nums', 'fav_nums', 'image' ]
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'click_nums', 'fav_nums', 'image',
                   'add_time']
    refresh_times = [3, 5]
    style_fields = {"detail": "ueditor"}

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()





class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourseAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResourse, CourseResourseAdmin)