from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    USER_GENDER_TYPE = (
        ('male', '男'), (
            'female', '女')
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')  #一对一关系
    # username = models.CharField("用户名", max_length=10, blank=True, default='')  #为了点赞功能实现的model行
    nike_name = models.CharField(verbose_name='昵称', max_length=50, blank=True, default='')
    desc = models.TextField('个人简介', max_length=200, blank=True, default='')
    gexing = models.CharField('个人签名', max_length=100, blank=True, default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', max_length=6, choices=USER_GENDER_TYPE,
                              default='male')
    address = models.CharField(verbose_name='地址', max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.png',
                              max_length=100, verbose_name='用户头像')

    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username


class EmailVerifyRecord(models.Model):
    """"邮箱验证记录"""
    SEND_TYPE_CHOICES = (
        ('register', '注册'),
        ('forget ', '找回密码'),
    )
    #
    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, max_length=10,
                                 default='register ')
    send_time = models.DateTimeField('时间', auto_now_add=True)

    #
    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    #
    def __str__(self):
        return self.code


#
# from django.db import models
#
#
# # Create your models here.
# class BlogPost(models.Model):
#     title = models.CharField(max_length=150)  # 博客的标题
#     body = models.TextField()  # 博客正文
#     timestamp = models.DateTimeField()  # 博客创建时间


# users/models.py

class UserInfos(models.Model):
    username = models.CharField("用户名", max_length=100)
    email = models.EmailField("邮箱", unique=True)

    # 其他字段

    def __str__(self):
        return self.username
