from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from django.core.paginator import Paginator
from .models import Category, Post, Comment, LikeNum, Link
# Discussion, Fav, FavNum, Reply,
from .forms import CommentForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
# from .users.models import UserProfile
from django.http import HttpResponseRedirect
from django.http import JsonResponse  #点赞功能
from django.views.decorators.http import require_POST  #点赞功能
from django.views.decorators.csrf import csrf_exempt


def link_list(request):
    return {
        'link_list': Link.objects.all()
    }


def index(request):
    per_page = int(request.GET.get('per_page', 2))  # 默认每页显示4条
    print(f"Requested per_page: {per_page}")  # 调试输出
    post_list = Post.objects.all()
    paginator = Paginator(post_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'per_page': per_page}
    return render(request, 'blog/base.html', context)


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # 获取当前分类下的所有文章
    posts = category.post_set.all()
    per_page = request.GET.get('per_page', 2)
    paginator = Paginator(posts, per_page)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj, 'per_page': per_page}
    return render(request, 'blog/list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 每次刷新页面时，视图计数加1
    post.views_count += 1
    post.save()

    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, '您的评论已成功添加！')
            return redirect(reverse('blog:post_detail', args=[post_id]))

    # 使用POST / Redirect / GET模式。在用户提交表单后，视图会先处理表单数据，然后重定向到一个新的页面（通常是同一个页面），这样用户在刷新页面时不会重复提交表单。
    # 修改post_detail视图：确保在你的视图函数中，在成功处理评论提交后使用HttpResponseRedirect来重定向用户。

    else:
        comment_form = CommentForm()

    template = 'blog/post/detail.html'
    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
        'prev_post': Post.objects.filter(id__lt=post.id).order_by('-id').first(),
        'next_post': Post.objects.filter(id__gt=post.id).order_by('id').first(),
    }

    return render(request, template, context)


def search(request):
    """ 搜索视图 """
    keyword = request.GET.get('keyword')
    per_page = request.GET.get('per_page', 2)
    # 没有搜索默认显示所有文章
    if not keyword:
        post_list = Post.objects.all()
    else:
        # 包含查询的方法，用Q对象来组合复杂查询，title__icontains 他两个之间用的是双下划线（__）链接
        post_list = Post.objects.filter(
            Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'keyword': keyword
    }
    return render(request, 'blog/index.html', context)


def archives(request, year, month):
    # 文章归档列表页
    post_list = Post.objects.filter(add_date__year=year, add_date__month=month)
    per_page = request.GET.get('per_page', 2)
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'year': year, 'month': month, 'per_page': per_page}
    return render(request, 'blog/archives_list.html', context)


def findCurrentUser(request):
    # 实现你的逻辑来获取当前用户
    return request.user if request.user.is_authenticated else None


def home(request):
    link_list = Link.objects.all()
    print("Debug: link_list = ", link_list)  # 调试信息
    for link in link_list:
        print(link.title, link.url)  # 打印每个链接的信息
    return render(request, 'blog/base.html', {'link_list': link_list})


# 讨论点赞
from django.db import transaction

# def like_discussion(request, discussion_id):
#     if request.method == 'POST':
#         print('Received POST request')
#         discussion = get_object_or_404(id=discussion_id)
#         user = request.user
#         liked = LikeNum.objects.filter(user=user, discussion=discussion).exists()
#
#         if liked:
#             print('User already liked, removing like')
#             LikeNum.objects.filter(user=user, discussion=discussion).delete()
#             discussion.likenum -= 1
#             discussion.save()
#             status = 'unliked'
#         else:
#             print('Adding like')
#             LikeNum.objects.create(user=user, discussion=discussion)
#             discussion.likenum += 1
#             discussion.save()
#             status = 'liked'
#
#         return JsonResponse({'status': status, 'likenum': discussion.likenum})


# def post_detail(request, post_id):
#     # 文章详情页
#     post = get_object_or_404(Post, id=post_id)
#
#     # 用文章id来实现的上下篇
#     prev_post = Post.objects.filter(id__lt=post_id).last()  # 上一篇
#     next_post = Post.objects.filter(id__gt=post_id).first() # 下一篇
#     Post.objects.filter(id=post_id).update(pv = F('pv') + 1)   # 这个功能有漏洞，仅做思路讲解
#
#     # 用发布日期来实现上下篇
#     # date_prev_post = Post.objects.filter(add_date__lt=post.add_date).last()
#     # date_next_post = Post.objects.filter(add_date__gt=post.add_date).first()
#
#     context = {'post': post, 'prev_post': prev_post, 'next_post': next_post}
#     return render(request, 'blog/detail.html', context)
