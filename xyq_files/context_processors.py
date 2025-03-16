from xyq_files.models import Reply

def unread_count_processor(request):
    if request.user.is_authenticated:
        unread_count = Reply.objects.filter(entry__owner=request.user, is_read=False).count()
    else:
        unread_count = 0
    return {'unread_count': unread_count}