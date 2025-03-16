from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

# 获取自定义用户模型
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # 绑定到自定义用户模型
        fields = ('username','email','phone_number','password1', 'password2')  # 包含需要的字段


class IntroductionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['introduction']  # 只包含需要编辑的字段
        labels = {
            'introduction': '个人简介',  # 自定义字段标签
        }
        widgets = {
            'introduction': forms.Textarea(attrs={
                'class': 'form-control',  # 添加 CSS 类
                'rows': 4,  # 设置文本框行数
                'placeholder': '请输入您的个人简介...',  # 添加占位符
            }),
        }
class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("该用户名已被使用，请选择其他用户名。")
        return username