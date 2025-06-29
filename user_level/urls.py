from django.urls import path
from .views import daily_check_in

app_name = 'user_level'

urlpatterns = [
    path('check-in/', daily_check_in, name='daily_check_in'),
]    