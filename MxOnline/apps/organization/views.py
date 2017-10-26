# _*_ coding:utf-8 _*_
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from pure_pagination import PageNotAnInteger, Paginator
# Create your views here.
from django.views.generic import View

from courses.models import Course
from operation.models import UserFavorite
from organization.forms import UserAskForm
from organization.models import CourseOrg, CityDict, Teacher


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 城市
        all_citys= CityDict.objects.all()
        # 机构搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        category = request.GET.get('ct', '')
        if category:
            all_orgs = CourseOrg.objects.filter(category=category)
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = CourseOrg.objects.filter(city_id=int(city_id))
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'course_nums':
            all_orgs = all_orgs.order_by('-course_nums')
        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort

        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        mobile = request.POST.get("mobile")
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg": "添加出错"}', content_type='application/json' )


class OrgHomeView(View):
    """机构首页"""
    def get(self, request, course_org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(course_org_id))
        # 点击数
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_org.id):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,

        })


class OrgCourseView(View):
    """机构课程"""
    def get(self, request, course_org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(course_org_id))
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page
        })


class OrgDescView(View):
    """机构详情"""
    def get(self, request, course_org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(course_org_id))
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page
        })

class OrgTeacherView(View):
    """机构讲师"""

    def get(self, request, course_org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(course_org_id))
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page

        })


class AddFvaView(View):
    def post(self, request):
        fav_type = request.POST.get('fav_type', 0)
        fav_id = request.POST.get('fav_id', 0)
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_type=int(fav_type), fav_id=int(fav_id))
        if exist_records:
            exist_records.delete()
            # 收藏数
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            if int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            if int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"fail", "msg":"收藏"}', content_type='application/json')
        else:
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums += 1
                course.save()
            if int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums += 1

                org.save()
            if int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums += 1
                teacher.save()

            if int(fav_id) > 0 and int(fav_type) > 0:
                # 收藏数
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_type = int(fav_type)
                user_fav.fav_id = int(fav_id)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()
        # 讲师搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords))

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')

        sorted_teachers = all_teachers.order_by('-click_nums')[:3]
        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 2, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'teacher_nums': teacher_nums,
            'sorted_teachers': sorted_teachers,
            'sort': sort,
        })


class TeacherDetailView(View):
    """讲师详情"""
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        # 点击数
        teacher.click_nums += 1
        teacher.save()
        courses = Course.objects.filter(teacher=teacher)

        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        has_teacher_fav = False
        has_org_fav = False
        if request.user.is_authenticated():

            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_teacher_fav = True

            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_org_fav = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'courses': courses,
            'teacher_id': teacher_id,
            'sorted_teachers': sorted_teachers,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav,

        })