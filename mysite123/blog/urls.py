from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [  # 用于将特定的 URL 路由映射到对应的views.py
    path('', views.index, name='index'),  # 访问网站根目录
    path('category/<int:category_id>/', views.category_list, name='category_list'),  # 访问特定分类下的文章列表
    path('search/', views.search, name='search'),  # 处理搜索功能的请求
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),  # 表示特定年份和月份的归档文章
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('home/', views.home, name='home'),  # 显示主页或自定义的首页内容
    # path('discussion/<int:discussion_id>/like/', views.like_discussion, name='like_discussion'),  # 特定讨论的 ID，用于处理讨论点赞功能
]

# 这些 URL 路由定义后，可以在 Django 模板中通过 {% url 'blog:index' %} 等方式引用这些 URL。例如
