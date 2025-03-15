"""为应用程序自定义URL模式"""

from django.urls import path,include

from . import views

app_name='users'
urlpatterns = [
    #包含默认身份信息验证URL
    path('',include('django.contrib.auth.urls')),
    #注册页面
    path('register/',views.register,name='register'),
    #个人主页
    path('user/<int:user_id>',views.introduction,name='introduction'),
    #修改简介
    path('edit_introduction/<int:user_id>',views.edit_introduction,name='edit_introduction')
]