# !/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from PyQt5.QtCore import pyqtSignal, QObject

from commun.utils.timestamp import timestamp_at_day_ago
from commun.model.plan_prod import PlanProd


class PlanProdStore(QObject):
    SETTINGS_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(PlanProdStore, self).__init__()

    def get_plan_prod(self):
        return PlanProd(start=0)


plan_prod_store = PlanProdStore()
