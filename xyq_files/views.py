from django.shortcuts import render,redirect
from .models import Topic,Entry,Reply
from .forms import EntryForm,ReplyForm
from django.contrib.auth.decorators import login_required

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
def new_entry(request,topic_id):
    """在特定板块中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #未提交数据，创建一个空表单
        form = EntryForm()

    else:
        #post提交的数据：对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('xyq_files:topic',topic_id = topic_id)
        
    #显示空表单或指出表单数据无效
    context={'topic':topic,'form':form}
    return render(request,'xyq_files/new_entry.html',context)

def entry(request,entry_id):
    """显示单个条目的所有回复"""
    entry = Entry.objects.get(id=entry_id)
    replies = entry.reply_set.order_by('-date_added')
    context = {'entry':entry,'replies':replies}
    return render(request,'xyq_files/entry.html',context)

@login_required
def new_reply(request,entry_id):
    """给特定帖子评论"""
    entry = Entry.objects.get(id=entry_id)

    if request.method != 'POST':
        #未提交数据，创建一个空表单
        form = ReplyForm()

    else:
        #post提交的数据：对数据进行处理
        form = ReplyForm(data=request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.entry = entry
            new_reply.owner = request.user 
            new_reply.save()
            return redirect('xyq_files:entry',entry_id = entry_id)
        
    #显示空表单或指出表单数据无效
    context={'entry':entry,'form':form}
    return render(request,'xyq_files/new_reply.html',context)

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
    unread_reply = Reply.objects.filter(entry__owner=request.user, is_read=False)
    unread_reply = unread_reply.order_by('-date_added')
    return render(request, 'xyq_files/unread_messages.html', {'unread_messages':unread_reply})


@login_required
def some_view(request):
    # 获取当前用户的未读消息数量
    unread_count = Reply.objects.filter(entry__owner=request.user, is_read=False).count()
    print(unread_count)
    # 将未读消息数量传递给模板
    return render(request, 'xyq_files/base.html', {'unread_count': unread_count})

@login_required
def mark_all_as_read(request):
    # 获取当前用户的所有未读消息
    unread_messages = Reply.objects.filter(entry__owner=request.user, is_read=False)
    
    # 将所有未读消息标记为已读
    unread_messages.update(is_read=True)
    
    # 重定向到消息列表页面
    return redirect('xyq_files:unread_messages')

@login_required
def all_messages(request):
    # 获取当前用户的未读消息
    reply = Reply.objects.filter(entry__owner=request.user)
    reply = reply.order_by('-date_added')
    return render(request, 'xyq_files/all_messages.html', {'all_messages':reply})