from django.shortcuts import render,redirect
from .models import Topic,Entry,Reply,CustomUser
from .forms import EntryForm,ReplyForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from itertools import chain

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
def some_view(request):
    # 获取当前用户的未读消息数量
    unread_entries = Entry.objects.filter(receiver=request.user, is_read=False).count()
    unread_replies = Reply.objects.filter(entry__owner=request.user, is_read=False).count()
    unread_replies1 = Reply.objects.filter(receiver=request.user, is_read=False).count()

    unread_count = unread_entries + unread_replies + unread_replies1
    print(unread_count)
    # 将未读消息数量传递给模板
    return render(request, 'xyq_files/base.html', {'unread_count': unread_count})

@login_required
def mark_all_as_read(request):
    # 将所有未读消息标记为已读
    Entry.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    # 标记Reply中的未读消息
    Reply.objects.filter(entry__owner=request.user, is_read=False).update(is_read=True)
    Reply.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    # 重定向到消息列表页面
    return redirect('xyq_files:unread_messages')

@login_required
def all_messages(request):
    # 获取当前用户的所有消息
    entries = Entry.objects.filter(receiver=request.user).order_by('-date_added')
    replies = Reply.objects.filter(entry__owner=request.user).order_by('-date_added')
    replies1 = Reply.objects.filter(receiver=request.user, is_read=False).order_by('-date_added')

    message = list(entries) + list(replies) + list(replies1)
    return render(request, 'xyq_files/all_messages.html', {'all_messages':message})