from .models import Entry, Reply
from users.models import PrivateMessage  # 导入私聊消息模型

def unread_count_processor(request):
    if request.user.is_authenticated:
        # 未读回复计数（两种类型）
        unread_replies1 = Reply.objects.filter(receiver=request.user, is_read=False).count()
        unread_replies2 = Reply.objects.filter(entry__owner=request.user, is_read=False).count()
        
        # 未读条目计数
        unread_entries = Entry.objects.filter(receiver=request.user, is_read=False).count()
        
        # 未读私聊消息计数
        unread_private_messages = PrivateMessage.objects.filter(
            receiver=request.user, 
            is_read=False
        ).count()
        
        # 总未读数
        total_unread = (
            unread_entries + 
            unread_replies1 + 
            unread_replies2 + 
            unread_private_messages
        )
        
        return {
            'unread_count': total_unread,
            'unread_private_messages': unread_private_messages  # 单独暴露私聊未读数，可选
        }
    return {
        'unread_count': 0,
        'unread_private_messages': 0
    }