#-*- coding: utf-8 -*-
from django import template
from datetime import datetime

register = template.Library()

def mytimesince_filter(value):
    result = "刚刚"
    now = datetime.now()
    days = now.day - value.day
    hours = now.hour-value.hour
    minutes=now.minute-value.minute
    seconds=now.second-value.second
    if days != 0:
        result = str(days)+"天前"
    elif hours !=0:
        result = str(hours)+"小时前"
    elif minutes != 0:
        result = str(minutes)+"分钟前"
    elif seconds != 0:
        result = str(seconds)+"秒前"
    return result

register.filter('mytimesince', mytimesince_filter)