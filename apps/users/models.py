# *_* coding:utf-8 *_*
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):   #继承django默认的AbstractUser表
    nick_name = models.CharField(verbose_name=u"用户昵称", max_length=50, default="")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(verbose_name=u"性别", max_length=10, choices=(("male", u"男"), ("female", u"女")), default="female")
    address = models.CharField(verbose_name=u"居住地址", max_length=100, default="")
    mobile = models.CharField(verbose_name=u"手机号", max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name=u"头像", upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)


    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    #获取用户未读消息的数量
    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(choices=(("register", u"注册"), ("forget", u"找回密码"), ("update_email", u"修改邮箱")), max_length=30, verbose_name=u"验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")


    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100,  verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name