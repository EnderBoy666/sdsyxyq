from django.contrib.auth import login
from django.contrib.auth import get_user_model
from .models import CustomUser
from .forms import CustomUserCreationForm,IntroductionForm  # 导入自定义表单
from django.http import Http404
from xyq_files.models import Entry
from django.contrib.auth.decorators import login_required
from .forms import ChangeUsernameForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash  # 用于保持用户登录状态
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser



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
    return render(request,'introduction/introduction.html',context)

@login_required
def edit_profile(request, user_id):
    # 获取当前用户对象
    user = get_object_or_404(CustomUser, id=user_id)
    
    # 确保当前登录用户只能修改自己的资料
    if request.user != user:
        raise Http404

    # 初始化三个表单
    username_form = ChangeUsernameForm(instance=user)
    introduction_form = IntroductionForm(instance=user)
    password_form = PasswordChangeForm(user=user)

    if request.method == 'POST':
        # 根据提交的按钮判断是哪个表单提交的
        if 'change_username' in request.POST:
            username_form = ChangeUsernameForm(request.POST, instance=user)
            if username_form.is_valid():
                username_form.save()
                return redirect('users:edit_profile', user_id=user.id)
        
        elif 'change_introduction' in request.POST:
            introduction_form = IntroductionForm(request.POST, instance=user)
            if introduction_form.is_valid():
                introduction_form.save()
                return redirect('users:edit_profile', user_id=user.id)
        
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # 保持用户登录状态
                return redirect('users:edit_profile', user_id=user.id)

    # 渲染模板
    return render(request, 'introduction/edit_profile.html', {
        'username_form': username_form,
        'introduction_form': introduction_form,
        'password_form': password_form,
        'user': user,
    })

