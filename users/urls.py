"""为应用程序自定义URL模式"""

from django.urls import path,include
from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from . import views
from .views import edit_profile

app_name='users'
urlpatterns = [
    #包含默认身份信息验证URL
    path('',include('django.contrib.auth.urls')),
    #注册页面
    path('register/',views.register,name='register'),
    #个人主页
    path('user/<int:user_id>',views.introduction,name='introduction'),
    #修改资料
    path('edit_profile/<int:user_id>/', edit_profile, name='edit_profile'),
]