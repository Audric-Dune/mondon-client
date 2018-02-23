# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.utils.timestamp import timestamp_to_day


def is_weekend(ts_day):
    """
    Test si un ts correspond à un jour du weekend (samedi ou dimanche)
    :return: True si le ts correspond a un samedi ou dimanche sinon False
    """
    day = timestamp_to_day(ts_day)
    return day == "samedi" or day == "dimanche"


def is_vendredi(ts_day):
    """
    Test si un ts correspond à vendredi
    :return: True si le ts correspond à vendredi sinon False
    """
    day = timestamp_to_day(ts_day)
    return day == "vendredi"
