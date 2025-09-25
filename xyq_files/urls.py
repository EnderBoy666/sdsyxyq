"""定义校园墙的URL模式"""

from django.urls import path

from . import views

from django.views.generic.base import RedirectView

app_name = 'xyq_files'
urlpatterns = [
    #图标
    #path(r'favicon.ico',RedirectView.as_view(url=r'favicon.ico')),
    #主页
    path('',views.index,name='index'),
    #显示所有主题
    path('topics/',views.topics,name='topics'),
    #特定主题的详细界面
    path('topics/<int:topic_id>/', views.topic,name='topic'),
    #用于添加新条目的页面
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
    #特定条目的详细界面
    path('entry/<int:entry_id>/', views.entry,name='entry'),
    #用于添加回复的页面
    path('new_reply/<int:entry_id>/',views.new_reply,name='new_reply'),
    #下载
    path('downloads',views.download,name='downlaod'),
    #未读消息
    path('unread_messages',views.unread_messages,name='unread_messages'),
    #标为已读
    path('mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),
    #全部消息
    path('all_messages',views.all_messages,name='all_messages'),
    #搜索用户
    path('search_users/', views.search_users, name='search_users'),
    #用户须知
    path('EULA/',views.eula,name='EULA'),
    path('about_us/',views.about_us,name='about_us'),
    # 添加赞助页面路由
    path('sponsor_us/', views.sponsor_us, name='sponsor_us'),
]