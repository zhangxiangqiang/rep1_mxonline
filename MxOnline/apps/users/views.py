# _*_ coding:utf-8 _*_
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password


from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import PageNotAnInteger, Paginator

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetForm, ResetForm, ImageUploadForm, UsercenterInfoForm
from users.models import UserProfile, EmailVerifyRecord, Banner
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class IndexView(View):
    def get(self, request):
        all_banners =Banner.objects.all().order_by('index')[:3]
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,

        })


class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse("index"))



class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse("index"))
                    # return render(request, "index.html", {})
                else:
                    return render(request, "login.html", {'msg': '用户未激活'})
            else:
                return render(request, "login.html", {'msg': '用户名或密码错误'})
        else:
            return render(request, "login.html", {"login_form": login_form})


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})
# 由于RegisterView没有判重，自己试着加一个逻辑
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            # 自己加的判重逻辑
            user = UserProfile.objects.filter(Q(username=user_name) | Q(email=user_name))
            if user:
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户名已存在'})

            else:
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.is_active = False
                user_profile.password = make_password(pass_word)
                user_profile.save()

                # 发送用户信息
                user_message = UserMessage()
                user_message.user = user_profile.id
                user_message.message = "欢迎注册慕课网"
                user_message.save()

                send_register_email(user_name, "register")
                return render(request, "login.html", {'msg': '邮件已发送，请到邮箱激活你的账号'})
        else:
             return render(request, 'register.html', {'register_form': register_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, 'send_success.html')
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'password_reset.html', {"email": email})
        else:
            return render(request, 'active_fail.html')
        return  render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)#不理解
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {"email": email, "reset_form": reset_form})


class UsercenterInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        usercenterinfo_form = UsercenterInfoForm(request.POST, instance=request.user)
        if usercenterinfo_form.is_valid():
            usercenterinfo_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse(json.dumps(usercenterinfo_form.errors), content_type='application/json')


class ImageUploadView(View):
    def post(self, request):
        image_upload_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_upload_form.is_valid():
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdatePwdView(View):
    """用户中心修改密码"""
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            request.user.password = make_password(pwd2)
            request.user.save()
            return HttpResponse('{"status":"success", "msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """发送邮箱验证码"""
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已经存在"}', content_type='application/json')
        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(View):
    """修改邮箱"""
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        existed_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email")
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return  HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"email": "验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """用户课程"""
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """用户收藏机构"""
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """用户收藏讲师"""
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list,
        })

class MyFavCourseView(LoginRequiredMixin, View):
    """用户收藏课程"""

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    """用户消息"""

    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        for message in all_messages:
            message.has_read = True
            message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 8, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "all_messages": messages,
        })


def page_not_found(request):
    """404全局处理"""
    from django.shortcuts import  render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

def page_error(request):
    """500全局处理"""
    from django.shortcuts import  render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response