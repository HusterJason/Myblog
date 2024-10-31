from django.contrib import admin  # 从 Django 的 contrib 模块中导入 admin，用于管理后台功能

# Register your models here.  # 提示在此处注册你的模型到管理后台
from .models import Category, Post, Tag, Sidebar, Comment, Link  # 从当前目录下的 models.py 文件中导入模型

admin.site.register(Category)  # 将 Category 模型注册到 Django 管理后台
admin.site.register(Tag)
admin.site.register(Sidebar)
admin.site.register(Link)


class PostAdmin(admin.ModelAdmin):  # 定义一个自定义的管理类 PostAdmin，继承自 admin.ModelAdmin
    list_display = ('id', 'title', 'category', 'tags', 'owner', 'pv', 'is_hot', 'pub_date',)  # 定义在列表页面显示的字段
    list_filter = ('owner',)  # 定义可以用来过滤的字段
    search_fields = ('title', 'desc')  # 搜索的字段
    list_editable = ('is_hot',)  # 列表页面直接编辑的字段
    list_display_links = ('id', 'title',)  # 哪些字段可以点击进入详情页面

    # class Media:  # 定义一个内嵌的 Media 类，用于在管理后台页面中添加自定义的 CSS 和 JS
    #     css = {
    #         'all': ('ckeditor5/cked.css',)  # 引入自定义的 CSS 文件
    #     }
    #     js = (
    #         'https://cdn.bootcdn.net/ajax/libs/jquery/3.7.1/jquery.js',  # 引入 jQuery 库
    #         'ckeditor5/ckeditor.js',  # 引入 CKEditor 库
    #         'ckeditor5/translations/zh.js',  # 引入 CKEditor 的中文翻译
    #         'ckeditor5/config.js',  # 引入自定义的 CKEditor 配置
    #     )


@admin.register(Comment)  # 使用 @admin.register 装饰器将 Comment 模型注册到管理后台，并指定使用 CommentAdmin 进行管理
class CommentAdmin(admin.ModelAdmin):  # 定义一个自定义的管理类 CommentAdmin，继承自 admin.ModelAdmin
    list_display = ('name', 'email', 'post', 'created', 'active')  # 定义在列表页面显示的字段
    list_filter = ('active', 'created', 'updated')  # 定义可以用来过滤的字段
    search_fields = ('name', 'email', 'body')  # 定义可以用来搜索的字段


admin.site.register(Post, PostAdmin)  # 将 Post 模型注册到 Django 管理后台，并指定使用自定义的 PostAdmin 进行管理

