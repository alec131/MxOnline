# *_*coding:utf-8 *_*
__author__ = 'Alec1312'
__date__ = '2018/4/6 15:36' 

import xadmin
from xadmin import views
from .models import EmailVerifyRecord,Banner, UserProfile

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = u"后台管理系统"
    site_footer = u"Django在线"
    menu_style = "accordion"

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type', 'send_time']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-envelope'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    model_icon = 'fa fa-picture-o'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)