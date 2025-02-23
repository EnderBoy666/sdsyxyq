from django.shortcuts import render,redirect
from .models import Topic,Entry,Reply
from .forms import EntryForm,ReplyForm

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
    context ={'topic': topic,'entries': entries}
    return render(request,'xyq_files/topic.html',context)

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


