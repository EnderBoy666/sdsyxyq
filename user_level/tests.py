from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

User = get_user_model()  # 使用Django推荐的方式获取用户模型

class DailyCheckInTestCase(TestCase):
    def setUp(self):
        # 使用get_user_model()创建用户实例
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
    def test_first_check_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/user_level/check-in/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['data']['consecutive_days'], 1)
        
        # 验证数据库更新
        user = User.objects.get(username='testuser')
        self.assertEqual(user.points, 5)
        self.assertEqual(user.consecutive_check_in_days, 1)
        self.assertEqual(user.last_check_in.date(), timezone.now().date())
    
    def test_consecutive_check_in(self):
        # 设置上次签到时间为昨天
        user = User.objects.get(username='testuser')
        user.last_check_in = timezone.now() - datetime.timedelta(days=1)
        user.consecutive_check_in_days = 3
        user.save()
        
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/user_level/check-in/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['data']['consecutive_days'], 4)
        
        # 验证数据库更新
        user = User.objects.get(username='testuser')
        self.assertEqual(user.points, 10)  # 原有0 + 新增10
        self.assertEqual(user.consecutive_check_in_days, 4)
    
    def test_already_checked_in_today(self):
        # 设置上次签到时间为今天
        user = User.objects.get(username='testuser')
        user.last_check_in = timezone.now()
        user.save()
        
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/user_level/check-in/')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')    