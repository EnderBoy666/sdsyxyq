from django.contrib import admin

from .models import Topic,Entry,Reply

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Reply)