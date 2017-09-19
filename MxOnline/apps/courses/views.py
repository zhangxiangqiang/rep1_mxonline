# _*_ coding:utf-8 _*_
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from django.views.generic import View
from pure_pagination import PageNotAnInteger, Paginator
from courses.models import Course, CourseResourse, Video
from operation.models import UserFavorite, CourseComment, UserCourse
from users.models import UserProfile
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses

        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 课程推荐
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,

        })


class CourseInfoView(LoginRequiredMixin, View):
    """课程视频信息"""

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查询用户是否关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        course_resources = CourseResourse.objects.filter(course=course)
        # 取出拥有此课程的用户课程对象
        user_courses = UserCourse.objects.filter(course=course)
        # 根据对象取出学习此课程的用户id,UserCourse中转
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据对象取出学习此课程的用户id,UserCourse中转
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        courses_ids = [user_course.course.id for user_course in all_user_courses]

        relate_courses = Course.objects.filter(id__in=courses_ids).order_by("-click_nums")[:5]

        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': course_resources,
            'relate_courses': relate_courses,

        })


class VideoPlayView(View):
    """视频播放"""
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        course_resources = CourseResourse.objects.filter(course=course)
        # 取出拥有此课程的用户课程对象
        user_courses = UserCourse.objects.filter(course=course)
        # 根据对象取出学习此课程的用户id,UserCourse中转
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据对象取出学习此课程的用户id,UserCourse中转
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        courses_ids = [user_course.course.id for user_course in all_user_courses]

        relate_courses = Course.objects.filter(id__in=courses_ids).order_by("-click_nums")[:5]

        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': course_resources,
            'relate_courses': relate_courses,
            'video': video,

        })

class CourseCommentsView(LoginRequiredMixin, View):
    """课程评论"""

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course_resources = CourseResourse.objects.filter(course=course)
        all_comments = CourseComment.objects.all()

        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': course_resources,
            'all_comments': all_comments,

        })


class AddCommentsView(View):
    """添加课程评论"""
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comments = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comments.user = request.user
            course_comments.course = course
            course_comments.comments = comments
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type="application/json")

