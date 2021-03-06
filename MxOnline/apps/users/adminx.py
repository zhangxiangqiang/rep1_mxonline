# _*_ coding:utf-8 _*_
import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner

__author__ = 'qing'
__date__ = '2017/7/26 16:33'


# class UserProfile
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    site_title = "学而强台管理系统"
    site_footer = "学而强在线网"
    menu_style = "accordion"
xadmin.site.register(views.CommAdminView, GlobalSettings)


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']
xadmin.site.register(Banner, BannerAdmin)