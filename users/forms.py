from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# 获取自定义用户模型
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # 绑定到自定义用户模型
        fields = ('username','email','phone_number','password1', 'password2')  # 包含需要的字段