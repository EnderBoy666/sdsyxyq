from .models import Entry, Reply

def unread_count_processor(request):
    if request.user.is_authenticated:
        unread_replies1 = Reply.objects.filter(receiver=request.user, is_read=False).count()
        unread_entries = Entry.objects.filter(receiver=request.user, is_read=False).count()
        unread_replies = Reply.objects.filter(entry__owner=request.user, is_read=False).count()
        return {'unread_count': unread_entries + unread_replies + unread_replies1}
    return {'unread_count': 0}