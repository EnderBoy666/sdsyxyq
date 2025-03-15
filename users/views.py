from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from .forms import CustomUserCreationForm,IntroductionForm  # 导入自定义表单
from django.http import Http404
from xyq_files.models import Entry


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

def introduction(request,user_id):
    user=CustomUser.objects.get(id=user_id)
    entries = Entry.objects.all()
    context ={'user1': user,'entries':entries}
    return render(request,'registration/introduction.html',context)

def edit_introduction(request, user_id):
    # 获取当前用户对象
    user = CustomUser.objects.get(id=user_id)
    if request.user != user:
        raise Http404

    if request.method == 'POST':
        # 如果是 POST 请求，处理表单数据
        form = IntroductionForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # 保存修改
            return redirect('users:introduction', user_id=user.id)  # 重定向到用户个人主页
    else:
        # 如果是 GET 请求，显示表单
        form = IntroductionForm(instance=user)

    # 渲染模板
    return render(request, 'registration/edit_introduction.html', {
        'form': form,
        'user': user,
    })
