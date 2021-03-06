# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import locale


def format_timedelta(td):
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)


def get_day_ago(timestamp):
    now = timestamp_now() - round(timestamp)
    return int(now / (3600 * 24))


def timestamp_to_inverse_date(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%Y_%m_%d')


def timestamp_to_hour(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')


def timestamp_to_hour_little(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%Hh%M')


def timestamp_to_date(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%A %d %B %Y')


def timestamp_to_date_little(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')


def timestamp_to_day_month_little(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%d/%m')


def timestamp_to_name_number_day_month(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%A %d/%m')


def timestamp_to_day(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%A')


def timestamp_to_week(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return 'Semaine {}'.format(datetime.fromtimestamp(timestamp).isocalendar()[1])


def timestamp_to_month(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%B - %Y')


def timestamp_to_month_little(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%B')


def timestamp_to_year(timestamp):
    locale.setlocale(locale.LC_TIME, '')
    return datetime.fromtimestamp(timestamp).strftime('%Y')


def hour_in_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M")


def get_hour_in_timestamp(ts):
    return datetime.fromtimestamp(ts).hour


def get_min_in_timestamp(ts):
    return datetime.fromtimestamp(ts).minute


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


def timestamp_after_day_ago(start, day_ago=0, hour=0):
    now = datetime.fromtimestamp(start) + timedelta(days=day_ago)
    return datetime(year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=hour,
                    minute=0,
                    second=0,
                    microsecond=0).timestamp()


def timestamp_at_week_ago(week_ago=0):
    day_ago_current_week = datetime.now().weekday()
    day_ago = day_ago_current_week + 7 * week_ago
    now = datetime.now() - timedelta(days=day_ago)
    return datetime(year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0).timestamp()


def timestamp_at_month_ago(month_ago=0):
    year = datetime.now().year
    month = datetime.now().month
    i = 0
    while i < month_ago:
        if month == 1:
            month = 12
            year = year - 1
        else:
            month -= 1
        i += 1
    return datetime(year=year,
                    month=month,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0).timestamp()


def timestamp_at_month(year_ago, month):
    current_year = datetime.now().year
    year = current_year - year_ago
    return datetime(year=year,
                    month=month,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0).timestamp()


def timestamp_at_year_ago(year_ago):
    current_year = datetime.now().year
    year = current_year - year_ago
    return datetime(year=year,
                    month=1,
                    day=1,
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


def is_vendredi(ts):
    """
    Test si le jour d'un timestamp est vendredi
    :param ts: Le timestamp a tester
    :return: True si on est vendredi
    """
    return timestamp_to_day(ts) == "vendredi"
