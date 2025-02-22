"""定义校园墙的URL模式"""

from django.urls import path

from . import views

app_name = 'xyq_files'
urlpatterns = [
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
]