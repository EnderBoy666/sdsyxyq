from django.http import HttpResponse
from django.utils import timezone
from .models import RequestLog, BannedIP
from .views import check_ban_ip
from django.shortcuts import redirect
from django.urls import resolve

class RequestLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取客户端 IP 地址
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # 检查 IP 是否已经被封禁
        try:
            banned_ip = BannedIP.objects.get(ip_address=ip)
            if timezone.now() < banned_ip.ban_end_time:
                return HttpResponse("This IP is still banned. Please try again later.", status=429)
            else:
                # 封禁时间已过，解除封禁
                banned_ip.delete()
        except BannedIP.DoesNotExist:
            pass

        # 记录请求
        RequestLog.objects.create(ip_address=ip)

        # 保留最近500条访问记录
        total_logs = RequestLog.objects.count()
        if total_logs > 500:
            logs_to_delete = total_logs - 500
            # 获取要删除的记录ID，避免直接使用limit进行delete
            oldest_log_ids = RequestLog.objects.order_by('request_time').values_list('id', flat=True)[:logs_to_delete]
            RequestLog.objects.filter(id__in=oldest_log_ids).delete()

        # 检查是否需要封禁 IP
        if check_ban_ip(ip):
            # 封禁 IP，例如封禁 10 分钟
            ban_end_time = timezone.now() + timezone.timedelta(minutes=10)
            BannedIP.objects.create(ip_address=ip, ban_end_time=ban_end_time)
            return HttpResponse("This IP is banned for excessive requests.", status=429)

        response = self.get_response(request)
        return response


class EULACheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(request, 'user') and request.user.is_authenticated:
            if not request.user.EULA_read:
                resolved_url = resolve(request.path_info)
                # 仅当不在EULA页面时才重定向
                if not (resolved_url.namespace == 'xyq_files' and resolved_url.url_name == 'EULA'):
                    return redirect('xyq_files:EULA')
        return response