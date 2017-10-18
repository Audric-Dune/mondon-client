# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import locale


def timestamp_to_hour(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')


def timestamp_to_hour_little(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%Hh%M')


def timestamp_to_date(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%A %d %B %Y')


def timestamp_to_day(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%A')


def timestamp_now():
    now = datetime.now()
    return datetime(year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=now.hour,
                    minute=now.minute,
                    second=now.second,
                    microsecond=now.microsecond).timestamp()


def timestamp_at_day_ago(day_ago=0):
    now = datetime.now() - timedelta(days=day_ago)
    return datetime(year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0).timestamp()


def timestamp_at_time(ts, hours=0, min=0, sec=0, microsecond=0):
    d = datetime.fromtimestamp(ts)
    return datetime(year=d.year,
                    month=d.month,
                    day=d.day,
                    hour=hours,
                    minute=min,
                    second=sec,
                    microsecond=microsecond).timestamp()


def timestamp_au_debut_de_hour(ts, min=0):
    d = datetime.fromtimestamp(ts)
    return datetime(year=d.year,
                    month=d.month,
                    day=d.day,
                    hour=d.hour,
                    minute=min,
                    second=0,
                    microsecond=0).timestamp()


def hour_in_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M")
