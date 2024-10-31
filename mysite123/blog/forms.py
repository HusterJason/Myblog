# forms.py
from django import forms
from .models import Comment
from .models import Post


# 评论
class CommentForm(forms.ModelForm):  # 定义了一个名为 CommentForm 的类，继承自 forms.ModelForm，用于创建基于 Comment 模型的表单
    class Meta: # 指定表单的元数据
        model = Comment # 指定表单基于 Comment 模型。这意味着表单的字段将对应 Comment 模型的字段。
        fields = ('name', 'email', 'body')    # 指定表单包含的字段为 name、email 和 body。这三个字段将显示在表单中
        labels = {
            'name': '名字',
            'email': 'Email邮箱',   # 为表单字段定义自定义标签
            'body': '内容',
        }
        widgets = {  # 为表单字段定义自定义的输入控件。每个控件都附加了一个 CSS 类，以便进行样式定制。
            'name': forms.TextInput(attrs={'class': 'input-transparent'}),
            'email': forms.EmailInput(attrs={'class': 'input-transparent'}),
            'body': forms.Textarea(attrs={'class': 'textarea-transparent'}),
        }
