from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from blog.models import Post

"""将此页所有email改成username就实现了邮箱、用户名登录基本功能"""


class LoginForm(forms.Form):
    # email = forms.CharField(label='用户名', max_length=32, widget=forms.TextInput(attrs={
    username = forms.CharField(label='用户名', max_length=32, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'}))

    def clean_password(self):
        # email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # if email == password:
        if username == password:
            raise forms.ValidationError('邮箱与密码不能相同!')
        return password


class RegisterForm(forms.ModelForm):
    # email = forms.CharField(label='邮箱', min_length=6, widget=forms.TextInput(attrs={
    email = forms.EmailField(label='邮箱', min_length=6, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '邮箱'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'}))
    password1 = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '再次输入密码'}))

    class Meta:
        """允许被编辑字段"""
        model = User
        fields = ['email', 'password']

    def clean_email(self):
        """ 验证用户存在 """
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password1(self):
        """验证两次密码"""
        if self.cleaned_data.get('password') != self.cleaned_data.get('password1'):
            raise forms.ValidationError('两次密码输入不一致！')
        return self.cleaned_data.get('password1')


class ForgetPwdForm(forms.Form):
    """ 填写email表单页面 """
    email = forms.EmailField(label='请输入注册邮箱地址', min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))


class ModifyPwdForm(forms.Form):
    """修改密码表单"""
    password = forms.CharField(label="输入新密码", min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': '输入密码'}))


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input', 'disabled': 'disabled'
    }))
    """允许被编辑字段"""

    class Meta:
        model = User
        fields = ['email']


class UserProfileForm(forms.ModelForm):
    """Form definition for UserInfo."""

    class Meta:
        """Meta definition for UserInfoform."""

        model = UserProfile
        fields = ('nike_name', 'desc', 'gexing', 'birthday', 'gender', 'address', 'image')


# class username(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username']

class PostForm(forms.ModelForm):  # 为了在前端页面中添加文章，需要一个 Django 表单
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

    def clean_category(self):
        category_id = self.cleaned_data.get('category')
        if not category_id:
            raise forms.ValidationError("Category is required.")
        return category_id
