from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from users.models import CustomUser
import datetime

# 新增：添加用户等级更新函数
def update_user_level(user):
    """根据用户积分更新用户等级"""
    if user.points < 100:
        user.level = 1
    elif user.points < 200:
        user.level = 2
    elif user.points < 500:
        user.level = 3
    elif user.points < 1000:
        user.level = 4
    else:
        user.level = 5
    user.save()

@login_required
def daily_check_in(request):
    user = request.user
    
    # 检查今日是否已签到
    if user.last_check_in and user.last_check_in.date() == timezone.now().date():
        return JsonResponse({
            'status': 'error',
            'message': '今日已签到，明天再来吧！',
            'data': {
                'points': user.points,
                'consecutive_days': user.consecutive_check_in_days
            }
        }, status=400)
    
    # 计算连续签到逻辑
    current_streak = user.consecutive_check_in_days
    
    # 如果上次签到是昨天，连续签到天数+1
    if user.last_check_in and (timezone.now().date() - user.last_check_in.date()) == datetime.timedelta(days=1):
        current_streak += 1
    # 否则重置连续签到
    else:
        current_streak = 1
    
    # 根据连续签到天数计算奖励积分
    if current_streak <= 3:
        reward_points = 5  # 连续1-3天，每天5积分
    elif current_streak <= 7:
        reward_points = 10  # 连续4-7天，每天10积分
    else:
        reward_points = 15  # 连续8天以上，每天15积分
    
    # 更新用户信息
    user.points += reward_points
    user.consecutive_check_in_days = current_streak
    user.last_check_in = timezone.now()
    user.save()
    
    # 更新用户等级
    update_user_level(user)
    
    return JsonResponse({
        'status': 'success',
        'message': f'签到成功！获得{reward_points}积分，连续签到{current_streak}天',
        'data': {
            'points': user.points,
            'consecutive_days': current_streak,
            'level': user.level
        }
    })    