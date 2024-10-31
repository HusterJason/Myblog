from django.contrib import admin

from .models import UserProfile, EmailVerifyRecord

# Register your models here.
admin.site.register(UserProfile)


@admin.register(EmailVerifyRecord)
class Admin(admin.ModelAdmin):
    list_display = ('code',)

# from mysite.blog import models  # 导入数据模型

#admin.site.register(models.BlogPost)  # 使用admin注册BlogPost类
