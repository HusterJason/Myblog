# blog/context_processors.py
from .models import Link


def link_list(request):
    return {
        'link_list': Link.objects.all()
    }

# 定义了一个名为 link_list 的函数，它接收一个 request 对象作为参数。作为一个上下文处理器（context processor）使用。
# 返回一个字典，字典的键为 'link_list'，值为 Link 模型的所有对象列表（Link.objects.all()）。这意味着在模板中可以通过 link_list 变量访问所有 Link 对象
# 上下文处理器：link_list 函数是一个上下文处理器，它会在每个模板渲染之前被调用，并将返回的字典数据添加到模板上下文中。
# 链接列表：通过这个上下文处理器，所有的模板都可以访问到 Link 模型的所有对象，这样就可以在任何模板中显示这些链接，例如在网站的侧边栏或页脚中显示友情链接。