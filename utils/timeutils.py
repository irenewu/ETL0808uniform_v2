# -*- coding: utf-8 -*-
"""tiem utils"""
import re
import time
from datetime import datetime as dt
from datetime import timedelta
import datetime

def timestamptostr(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
    """方法说明
    将时间戳转换为字符串格式的日期
    """
    if isinstance(timestamp, basestring):
        try:
            timestamp = float(timestamp)
        except:
            timestamp = ""
    if len(str(timestamp)) == 13:
        timestamp = timestamp/1000
    if not timestamp:
        return time.strftime(format_str)
    return time.strftime(format_str, time.localtime(timestamp))


def strtotimestamp(timestr, format_str="%Y-%m-%d %H:%M:%S"):
    """方法说明
    将字符串格式的日期转换为时间戳
    """
    return time.mktime(time.strptime(timestr, format_str))


def struct_time(timestamp=None):
    """方法说明
    将时间戳转换为时间对象，以便获取单独的年月日等信息
    """
    return time.localtime() if timestamp is None else time.localtime(timestamp)


def target_time(format_str="%Y-%m-%d %H:%M:%S", **kw):
    """方法说明
    利用datetime获取指定时间差的时间
    datetime.timedelta([days[, seconds[, microseconds[, milliseconds[,
    minutes[, hours[, weeks]]]]]]])
    """
    target_time = dt.now() + timedelta(**kw)
    return target_time.strftime(format_str)


def get_old_day(days=7, format_str="%Y-%m-%d"):

    today = dt.today()
    older = today - timedelta(days=days)

    return older.strftime(format_str), today.strftime(format_str)


def get_match_range_day(days=7, format_str="%Y-%m-%d"):

    today = dt.today()
    older = today - timedelta(days=days)
    newer = today + timedelta(days=days)

    return older.strftime(format_str), newer.strftime(format_str)


def get_old_hour(hours=12*60*60, format_str="%Y-%m-%d %H:%M:%S"):

    return time.strftime(format_str, time.localtime(time.time() - hours))


def get_publish_time(src=None):
    older, today = get_old_day(days=1)
    v_t = timestamptostr(timestamp="")
    if u"昨天" in src:
        v_t = older + src.replace(u"昨天", "") + ":00"
    if u"今天" in src:
        v_t = today + src.replace(u"今天", "") + ":00"
    if u"分钟" in src or u"秒" in src or u"小时" in src:
        delay = "".join(re.findall(re.compile(r'\d+', re.I), src))
        if u"分钟" in src:
            v_t = target_time(minutes=-int(delay))
        elif u"秒":
            v_t = target_time(seconds=-int(delay))
        else:
            v_t = target_time(hours=-int(delay))
    if len(src) == 11 and src.count("-") == 2:
        v_t = today.split("-")[0] + "-" + src + ":00"
    if len(src) == 16:
        v_t = src + ":00"
    return v_t

def getlast_threeweek(timestr, week_list=[]):
    """
    方法说明
    根据 timestr  为标准 获取前三周的第一天和最后一天
    比如 timestr 格式为 2017-07-03
    输出为 ['2017-05-01', '2017-06-01', '2017-07-01']
    :param timestr:
    :return:
    """
    if len(week_list) == 3:
        return week_list
    tr = timestr.split("-")
    d = dt(year=int(tr[0]), month=int(tr[1]), day=int(tr[2]))
    b = d - datetime.timedelta(d.weekday()+1)
    if not len(week_list):
        current_mond = d - datetime.timedelta(d.weekday())
        current_sund = current_mond + datetime.timedelta(6)
        week_list.append({current_mond.strftime("%Y-%m-%d"): current_sund.strftime("%Y-%m-%d")})
    days = []
    for i in range(6, -1, -1):
        c = b - datetime.timedelta(i)
        days.append(c.strftime("%Y-%m-%d"))
    week_list.append({days[0]: days[-1]})
    return getlast_threeweek(days[0], week_list)

def getlast_sevenday(timestr):
    """
        方法说明
        根据 timestr  为标准 获取前七天的时间
        比如 timestr 格式为 2017-07-03 为周一  获取上一周 周一-周天时间
        输出为 ['2017-06-27', '2017-06-28', '2017-06-29', '2017-06-30', '2017-07-01', '2017-07-02', '2017-07-03']
        :param timestr:
        :return:
        """
    tr = timestr.split("-")
    d = dt(year=int(tr[0]), month=int(tr[1]), day=int(tr[2]))
    days = []
    for i in range(6, -1, -1):
        b = str(d - datetime.timedelta(days=i)).split(" ")[0]
        days.append(b)
    return days

def getlast_threemonth(timestr):
    """
        方法说明
        根据 timestr  为标准 获取前三个月的时间
        比如 timestr 格式为 2017-07-03
        输出为 ['2017-05-01', '2017-06-01', '2017-07-01']
        :param timestr:
        :return:
        """
    tr = timestr.split("-")
    d = dt(year=int(tr[0]), month=int(tr[1]), day=int(tr[2]))
    d4 = d - datetime.timedelta(days=d.day)
    months = []
    for i in range(1, -1, -1):
        b = str(datetime.datetime(d4.year, d4.month-i, 1)).split(" ")[0]
        months.append(b)
    months.append(datetime.date(year=d.year, month=d.month, day=1).strftime("%Y-%m-%d"))
    return months