from django.contrib import admin
from users.models import Friendship, PrivateMessage,CustomUser

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

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # 显示的字段列表
    list_display = ('username', 'email', 'phone_number', 'points', 'level', 'last_check_in', 'consecutive_check_in_days', 'is_staff')
# 编辑表单中显示的字段集
fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('个人信息', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'introduction')}),
    ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    ('积分与等级', {'fields': ('points', 'level', 'last_check_in', 'consecutive_check_in_days')}),
    ('重要日期', {'fields': ('last_login', 'date_joined')}),
)

# 添加用户表单中显示的字段
add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'password1', 'password2', 'email', 'phone_number', 'points', 'level'),
    }),
)

# 可搜索的字段
search_fields = ('username', 'email', 'phone_number')

# 可过滤的字段
list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'level')

# 排序方式
ordering = ('-date_joined',)
