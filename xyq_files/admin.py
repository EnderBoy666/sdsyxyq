from django.contrib import admin
from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

        
from .models import Topic,Entry,Reply

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Reply)
admin.site.register(CustomUser,UserAdmin)