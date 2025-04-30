import unittest
from django.test import TestCase
from django.utils import timezone
from django.http import HttpRequest
from .models import RequestLog, BannedIP
from .middleware import RequestLimitMiddleware
from .views import check_ban_ip


class RequestLimitMiddlewareTest(TestCase):
    def setUp(self):
        self.middleware = RequestLimitMiddleware(lambda x: None)
        self.test_ip = '127.0.0.1'

    def test_check_ban_normal(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = self.test_ip
        # 模拟正常请求次数
        for _ in range(50):
            RequestLog.objects.create(ip_address=self.test_ip)
        response = self.middleware(request)
        self.assertEqual(response, None)  # 正常请求，中间件不应返回响应

    def test_check_ban_excessive(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = self.test_ip
        # 模拟超过阈值的请求次数
        for _ in range(150):
            RequestLog.objects.create(ip_address=self.test_ip)
        response = self.middleware(request)
        self.assertEqual(response.status_code, 429)  # 应返回 429 状态码，表示被封禁

    def test_banned_ip(self):
        # 先封禁 IP
        ban_end_time = timezone.now() + timezone.timedelta(minutes=10)
        BannedIP.objects.create(ip_address=self.test_ip, ban_end_time=ban_end_time)

        request = HttpRequest()
        request.META['REMOTE_ADDR'] = self.test_ip
        response = self.middleware(request)
        self.assertEqual(response.status_code, 429)  # 封禁状态下，应返回 429 状态码

    def test_ban_expired(self):
        # 先封禁 IP
        ban_end_time = timezone.now() - timezone.timedelta(minutes=10)  # 让封禁时间已过
        BannedIP.objects.create(ip_address=self.test_ip, ban_end_time=ban_end_time)

        request = HttpRequest()
        request.META['REMOTE_ADDR'] = self.test_ip
        response = self.middleware(request)
        self.assertEqual(response, None)  # 封禁时间已过，中间件不应返回响应


if __name__ == '__main__':
    unittest.main()