from django.shortcuts import render,redirect
from .models import Topic,Entry,Reply,CustomUser
from users.models import PrivateMessage,Friendship
from .forms import EntryForm,ReplyForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model,admin
from itertools import chain
from django.urls import reverse

# Create your views here.
def index(request):
    """校园墙的主页"""
    return render(request,'xyq_files/index.html')

def topics(request):
    """显示所有主题"""
    topics =Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request,'xyq_files/topics.html',context)

def topic(request,topic_id):
    """显示单个主题的所有条目"""
    topic =Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    for entry in entries:
        entry.reply_count = entry.reply_set.count()
    context ={'topic': topic,'entries': entries}
    return render(request,'xyq_files/topic.html',context)

@login_required
def new_entry(request, topic_id):
    """在特定板块中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('xyq_files:topic', topic_id=topic_id)
    
    context = {'topic': topic, 'form': form}
    return render(request, 'xyq_files/new_entry.html', context)

@login_required
def search_users(request):
    """搜索用户的AJAX视图"""
    query = request.GET.get('q', '')
    users = get_user_model().objects.filter(
        username__icontains=query
    ).exclude(id=request.user.id)[:10]  # 排除当前用户，限制10个结果
    
    results = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse(results, safe=False)

def entry(request,entry_id):
    """显示单个条目的所有回复"""
    entry = Entry.objects.get(id=entry_id)
    replies = entry.reply_set.order_by('-date_added')
    context = {'entry':entry,'replies':replies}
    return render(request,'xyq_files/entry.html',context)

@login_required
def new_reply(request, entry_id):
    """给特定帖子评论"""
    entry = Entry.objects.get(id=entry_id)

    if request.method != 'POST':
        form = ReplyForm()
    else:
        form = ReplyForm(data=request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.entry = entry
            new_reply.owner = request.user
            
            # 处理receiver字段
            if 'receiver' in request.POST and request.POST['receiver']:
                try:
                    receiver_id = int(request.POST['receiver'])
                    new_reply.receiver = CustomUser.objects.get(id=receiver_id)  # 直接使用CustomUser
                except (ValueError, CustomUser.DoesNotExist):
                    pass
            
            new_reply.save()
            return redirect('xyq_files:entry', entry_id=entry_id)
    
    context = {'entry': entry, 'form': form}
    return render(request, 'xyq_files/new_reply.html', context)

#下载文件
import os
from django.http import HttpResponse

def download(request):
    file_path = r'db.sqlite3'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            file_data = f.read()
        response = HttpResponse(file_data, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(file_path))
        return response
    else:
        return HttpResponse("Sorry, the file you requested does not exist.")



@login_required
def unread_messages(request):
    # 获取当前用户的未读消息

    unread_entries = Entry.objects.filter(receiver=request.user, is_read=False)
    unread_replies = Reply.objects.filter(entry__owner=request.user, is_read=False)
    unread_replies1 = Reply.objects.filter(receiver=request.user, is_read=False)

    combined_unread = list(unread_entries) + list(unread_replies) + list(unread_replies1)
    return render(request, 'xyq_files/unread_messages.html', {'unread_messages':combined_unread})


@login_required
def unread_messages(request):
    # 获取所有类型的未读消息
    unread_entries = Entry.objects.filter(receiver=request.user, is_read=False).order_by('-date_added')
    unread_replies_to_entries = Reply.objects.filter(entry__owner=request.user, is_read=False).order_by('-date_added')
    unread_replies_to_user = Reply.objects.filter(receiver=request.user, is_read=False).order_by('-date_added')
    unread_private_messages = PrivateMessage.objects.filter(receiver=request.user, is_read=False).order_by('-timestamp')
    unread_friend_requests = Friendship.objects.filter(to_user=request.user, is_accepted=False).order_by('-created_at')
    
    # 获取消息类型参数
    message_type = request.GET.get('type', 'all')
    
    # 根据类型过滤消息
    if message_type == 'entries':
        messages = list(unread_entries)
    elif message_type == 'replies_to_entries':
        messages = list(unread_replies_to_entries)
    elif message_type == 'replies_to_user':
        messages = list(unread_replies_to_user)
    elif message_type == 'private':
        messages = list(unread_private_messages)
    elif message_type == 'friend_requests':
        messages = list(unread_friend_requests)
    else:
        # 将所有消息合并，并添加类型标识和时间属性
        messages = []
        
        # 条目消息
        for msg in unread_entries:
            msg.msg_type = 'entry'
            msg.sort_time = msg.date_added
            messages.append(msg)
        
        # 回复条目消息
        for msg in unread_replies_to_entries:
            msg.msg_type = 'reply_to_entry'
            msg.sort_time = msg.date_added
            messages.append(msg)
        
        # 直接回复用户消息
        for msg in unread_replies_to_user:
            msg.msg_type = 'reply_to_user'
            msg.sort_time = msg.date_added
            messages.append(msg)
        
        # 私聊消息
        for msg in unread_private_messages:
            msg.msg_type = 'private'
            msg.sort_time = msg.timestamp
            messages.append(msg)
        
        # 好友请求
        for msg in unread_friend_requests:
            msg.msg_type = 'friend_request'
            msg.sort_time = msg.created_at
            messages.append(msg)
        
        # 按时间排序
        messages.sort(key=lambda x: x.sort_time, reverse=True)
    
    return render(request, 'xyq_files/unread_messages.html', {
        'unread_messages': messages,
        'current_type': message_type,
        'unread_counts': {
            'all': (unread_entries.count() + unread_replies_to_entries.count() + 
                   unread_replies_to_user.count() + unread_private_messages.count() +
                   unread_friend_requests.count()),
            'entries': unread_entries.count(),
            'replies_to_entries': unread_replies_to_entries.count(),
            'replies_to_user': unread_replies_to_user.count(),
            'private': unread_private_messages.count(),
            'friend_requests': unread_friend_requests.count(),
        }
    })

@login_required
def mark_all_as_read(request):
    # 获取类型参数
    message_type = request.GET.get('type', 'all')
    
    # 根据类型标记为已读
    if message_type == 'entries' or message_type == 'all':
        Entry.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    if message_type == 'replies_to_entries' or message_type == 'all':
        Reply.objects.filter(entry__owner=request.user, is_read=False).update(is_read=True)
    
    if message_type == 'replies_to_user' or message_type == 'all':
        Reply.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    if message_type == 'private' or message_type == 'all':
        PrivateMessage.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    if message_type == 'friend_requests' or message_type == 'all':
        # 好友请求标记为已读（接受或拒绝）
        # 这里可以根据需求决定是否自动接受或拒绝
        pass
    
    # 重定向回未读消息页面，保持当前筛选类型
    redirect_url = reverse('xyq_files:unread_messages')
    if message_type != 'all':
        redirect_url += f'?type={message_type}'
    return redirect(redirect_url)

@login_required
def all_messages(request):
    # 获取所有类型的消息
    entries = Entry.objects.filter(receiver=request.user).order_by('-date_added')
    replies_to_entries = Reply.objects.filter(entry__owner=request.user).order_by('-date_added')
    replies_to_user = Reply.objects.filter(receiver=request.user).order_by('-date_added')
    private_messages = PrivateMessage.objects.filter(receiver=request.user).order_by('-timestamp')
    
    # 获取消息类型参数
    message_type = request.GET.get('type', 'all')
    
    # 根据类型过滤消息
    if message_type == 'entries':
        messages = list(entries)
    elif message_type == 'replies_to_entries':
        messages = list(replies_to_entries)
    elif message_type == 'replies_to_user':
        messages = list(replies_to_user)
    elif message_type == 'private':
        messages = list(private_messages)
    else:
        messages = list(entries) + list(replies_to_entries) + list(replies_to_user) + list(private_messages)
    
    return render(request, 'xyq_files/all_messages.html', {
        'all_messages': messages,
        'current_type': message_type,
        'message_counts': {
            'all': entries.count() + replies_to_entries.count() + replies_to_user.count() + private_messages.count(),
            'entries': entries.count(),
            'replies_to_entries': replies_to_entries.count(),
            'replies_to_user': replies_to_user.count(),
            'private': private_messages.count(),
        }
    })