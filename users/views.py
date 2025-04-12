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
from django.contrib import messages as django_messages
from django.db.models import Q
from .models import CustomUser, Friendship, PrivateMessage
from .forms import FriendRequestForm, PrivateMessageForm




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

@login_required
def introduction(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    entries = Entry.objects.all()
    
    # 保留原有的回复计数功能
    for entry in entries:
        entry.reply_count = entry.reply_set.count()
    
    context = {
        'user1': user,
        'entries': entries,
        'is_own_profile': request.user.id == user.id  # 添加是否是自己的主页标志
    }
    
    # 如果是自己的主页，获取好友列表
    if context['is_own_profile']:
        # 获取已接受的好友关系
        friendships = Friendship.objects.filter(
            (Q(from_user=user) | Q(to_user=user)) & 
            Q(is_accepted=True)
        )
        
        friends = []
        for friendship in friendships:
            if friendship.from_user == user:
                friends.append(friendship.to_user)
            else:
                friends.append(friendship.from_user)
        
        context['friends'] = friends
        
        # 获取待处理的好友请求
        pending_requests = Friendship.objects.filter(
            to_user=user,
            is_accepted=False
        )
        context['pending_requests'] = pending_requests
    
    # 如果是他人主页，检查好友关系
    else:
        is_friend = Friendship.objects.filter(
            (Q(from_user=request.user, to_user=user) | 
             Q(from_user=user, to_user=request.user)) & 
            Q(is_accepted=True)
        ).exists()
        
        friend_request_sent = Friendship.objects.filter(
            from_user=request.user,
            to_user=user,
            is_accepted=False
        ).exists()
        
        context.update({
            'is_friend': is_friend,
            'friend_request_sent': friend_request_sent
        })
    
    return render(request, 'introduction/introduction.html', context)

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

@login_required
def friend_list(request):
    # 获取已接受的好友关系
    friendships = Friendship.objects.filter(
        (Q(from_user=request.user) | Q(to_user=request.user)) & 
        Q(is_accepted=True)
    )
    
    friends = []
    for friendship in friendships:
        if friendship.from_user == request.user:
            friends.append(friendship.to_user)
        else:
            friends.append(friendship.from_user)
    
    return render(request, 'chat/friend_list.html', {'friends': friends})

@login_required
def send_friend_request(request):
    initial_data = {}
    username = request.GET.get('username', None)
    
    if username:
        initial_data['username'] = username
    
    if request.method == 'POST':
        form = FriendRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            if username == request.user.username:
                django_messages.error(request, '你不能添加自己为好友')
                return redirect('users:send_friend_request')
            
            try:
                to_user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                django_messages.error(request, '用户不存在')
                return redirect('users:send_friend_request')
            
            # 检查是否已经是好友或已有请求
            existing_friendship = Friendship.objects.filter(
                (Q(from_user=request.user, to_user=to_user) | 
                 Q(from_user=to_user, to_user=request.user)))
            
            if existing_friendship.exists():
                django_messages.error(request, '好友请求已存在或已经是好友')
                return redirect('users:send_friend_request')
            
            # 创建好友请求
            Friendship.objects.create(
                from_user=request.user,
                to_user=to_user,
                is_accepted=False
            )
            django_messages.success(request, '好友请求已发送')
            return redirect('users:friend_list')
    else:
        form = FriendRequestForm(initial=initial_data)
    
    return render(request, 'chat/send_friend_request.html', {
        'form': form,
        'prefilled_username': username  # 传递给模板用于额外显示
    })

@login_required
def pending_requests(request):
    pending = Friendship.objects.filter(
        to_user=request.user,
        is_accepted=False
    )
    return render(request, 'chat/pending_requests.html', {'pending_requests': pending})

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(Friendship, id=request_id, to_user=request.user)
    friend_request.is_accepted = True
    friend_request.save()
    django_messages.success(request, f'你已接受 {friend_request.from_user.username} 的好友请求')
    return redirect('users:friend_list')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(Friendship, id=request_id, to_user=request.user)
    friend_request.delete()
    django_messages.success(request, f'你已拒绝 {friend_request.from_user.username} 的好友请求')
    return redirect('users:friend_list')

@login_required
def chat_with_friend(request, friend_id):
    friend = get_object_or_404(CustomUser, id=friend_id)
    
    # 检查是否是好友
    is_friend = Friendship.objects.filter(
        (Q(from_user=request.user, to_user=friend) | 
         Q(from_user=friend, to_user=request.user)) & 
        Q(is_accepted=True))
    
    if not is_friend.exists():
        django_messages.error(request, '你只能与好友聊天')
        return redirect('users:friend_list')
    
    messages = PrivateMessage.objects.filter(
        (Q(sender=request.user, receiver=friend) | 
         Q(sender=friend, receiver=request.user)))
    
    # 标记为已读
    PrivateMessage.objects.filter(sender=friend, receiver=request.user, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = friend
            message.save()
            return redirect('users:chat_with_friend', friend_id=friend.id)
    else:
        form = PrivateMessageForm()
    
    return render(request, 'chat/chat.html', {
        'friend': friend,
        'messages': messages,
        'form': form
    })
