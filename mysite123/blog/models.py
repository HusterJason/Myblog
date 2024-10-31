from django.db import models  # 从 django.db 导入 models 模块，用于定义数据库模型
from django.contrib.auth.models import User  # 从 django.contrib.auth.models 导入 User 模型，用于用户认证
from django.utils.functional import cached_property  # 从 django.utils.functional 导入 cached_property 装饰器，用于缓存属性
from django.template.loader import render_to_string  # 从 django.template.loader 导入 render_to_string 函数，用于渲染模板
from users.models import UserInfos  # 从 users 应用导入 UserInfos 模型
# 111

class Category(models.Model):
    """ 博客的分类模型 """
    name = models.CharField(max_length=32, verbose_name="分类名称")
    desc = models.TextField(max_length=200, blank=True, default='', verbose_name="分类描述")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        verbose_name = "博客分类"
        verbose_name_plural = verbose_name  # 设置模型的复数友好名称

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ 文章标签 """
    name = models.CharField(max_length=10, verbose_name="文章标签")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    """ 文章 """
    title = models.CharField(max_length=61, verbose_name="文章标题")
    desc = models.TextField(max_length=1000, blank=True, default='', verbose_name="文章描述")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    content = models.TextField(verbose_name="文章详情")
    tags = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.CASCADE, verbose_name="文章标签")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    is_hot = models.BooleanField(default=False, verbose_name="是否热门")  # 手动热门推荐
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    pv = models.IntegerField(default=0, verbose_name="浏览量")  # 浏览量
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    views_count = models.PositiveIntegerField(default=0)  #用于视图（眼睛）计数
    likes = models.IntegerField(default=0)  #添加一个字段用于存储点赞数
    liked_users = models.ManyToManyField(User, related_name='liked_posts', blank=True)  #添加一个字段用于存储哪些用户点赞了
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Sidebar(models.Model):  # admin 侧边栏的各类中
    # 侧边栏的模型数据

    STATUS = (
        (1, '隐藏'),
        (2, '展示')
    )

    DISPLAY_TYPE = (
        (1, '搜索'),
        (2, '最新文章'),
        (3, '最热文章'),
        (4, '最近评论'),
        (5, '文章归档'),
        (6, 'HTML')
    )

    title = models.CharField(max_length=50, verbose_name="模块名称")  # 模块名称
    display_type = models.PositiveIntegerField(default=1, choices=DISPLAY_TYPE,
                                               verbose_name="展示类型")  # 侧边栏  搜索框/最新文章/热门文章/HTML自定义等
    content = models.CharField(max_length=500, blank=True, default='', verbose_name="内容",
                               help_text="如果设置的不是HTML类型，可为空")  # 这个字段是专门用来给HTML类型用的，其他类型可为空
    sort = models.PositiveIntegerField(default=1, verbose_name="排序", help_text='序号越大越靠前')
    status = models.PositiveIntegerField(default=2, choices=STATUS, verbose_name="状态")  # 隐藏  显示状态
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  # 时间

    # models,DateTimeField(auto
    class Meta:
        verbose_name = "侧边栏"
        verbose_name_plural = verbose_name
        ordering = ['-sort']

    def __str__(self):
        return self.title

    @classmethod  # 类方法装饰器，这个就变成了这个类的一个方法可以调用
    def get_sidebar(cls):
        return cls.objects.filter(status=2)  # 查询到所有允许展示的模块

    @property  # 成为一个类属性，调用的时候不需要后边的（）,是只读的，用户没办法修改
    def get_content(self):
        if self.display_type == 1:
            context = {

            }
            return render_to_string('blog/sidebar/search.html', context=context)
        elif self.display_type == 2:
            context = {

            }
            return render_to_string('blog/sidebar/new_post.html', context=context)
        elif self.display_type == 3:
            context = {

            }
            return render_to_string('blog/sidebar/hot_post.html', context=context)
        elif self.display_type == 4:
            context = {

            }
            return render_to_string('blog/sidebar/commment.html', context=context)
        elif self.display_type == 5:  # 文章归档
            context = {

            }
            return render_to_string('blog/sidebar/archives.html', context=context)
        elif self.display_type == 6:  # 自定义侧边栏

            return self.content  # 在侧边栏直接使用这里的html，模板中必须使用safe过滤器去渲染HTML


#实现评论功能
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # 外键字段，关联到 Post 模型
    name = models.CharField(max_length=80)  # 评论者姓名
    email = models.EmailField()  # 评论者邮箱
    body = models.TextField()  # 评论内容
    created = models.DateTimeField(auto_now_add=True)  # 评论创建时间
    updated = models.DateTimeField(auto_now=True)  # 评论更新时间
    active = models.BooleanField(default=True)  # 评论是否激活

    class Meta:
        ordering = ('created',)  # 设置排序方式

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)  # 定义模型的字符串表示，返回评论者姓名和关联的文章标题


class Link(models.Model):  #友情链接
    title = models.CharField(max_length=100, verbose_name="链接标题")
    url = models.URLField(verbose_name="链接地址")
    description = models.TextField(blank=True, verbose_name="链接描述")

    def __str__(self):
        return self.title


# 喜欢数
class LikeNum(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    # discussion = models.ForeignKey(Discussion, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'user'

# class Data(models.Model):
#     question = models.CharField("问题", max_length=100, )
#     reply = models.CharField("回答", max_length=300)
#     likes = models.PositiveIntegerField('点赞数', default=0)
#     favs = models.PositiveIntegerField('收藏数', default=0)
#     created_time = models.DateTimeField("创建时间", auto_now_add=True)
#     updated_time = models.DateTimeField("更新时间", auto_now=True)
#
#     class Meta:
#         verbose_name_plural = 'Data'
#
#     def __str__(self):
#         return self.question
