from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm  # 导入自定义表单

def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = CustomUserCreationForm()  # 使用自定义表单
    else:
        # 处理提交的表单
        form = CustomUserCreationForm(data=request.POST)  # 使用自定义表单

        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，并重定向到主页
            login(request, new_user)
            return redirect('xyq_files:index')
    
    # 显示空表单或指出表单无效
    context = {'form': form}
    return render(request, 'registration/register.html', context)