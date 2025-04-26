from django.contrib import admin
from users.models import Friendship, PrivateMessage

# Register your models here.
@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'created_at', 'is_accepted')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('from_user__username', 'to_user__username')
    raw_id_fields = ('from_user', 'to_user')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    readonly_fields = ('created_at',)  # 设置为只读字段

    fieldsets = (
        ('基本信息', {
            'fields': ('from_user', 'to_user', 'is_accepted')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'short_content', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')
    raw_id_fields = ('sender', 'receiver')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    readonly_fields = ('timestamp',)  # 设置为只读字段

    fieldsets = (
        ('消息内容', {
            'fields': ('sender', 'receiver', 'content')
        }),
        ('状态信息', {
            'fields': ('is_read',),
            'classes': ('wide',)
        }),
        ('时间信息', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = '内容摘要'
    