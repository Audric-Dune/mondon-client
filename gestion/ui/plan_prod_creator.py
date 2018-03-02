# !/usr/bin/env python
# -*- coding: utf-8 -*-

# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QHBoxLayout

from commun.model.plan_prod import PlanProd
from commun.ui.public.mondon_widget import MondonWidget

from gestion.ui.selector import Selector


class PlanProdCreator(MondonWidget):

    def __init__(self, parent=None):
        super(PlanProdCreator, self).__init__(parent=parent)
        self.plan_prod = PlanProd()
        self.selector = Selector(plan_prod=self.plan_prod)
        self.init_ui()

    def init_ui(self):
        master_hbox = QHBoxLayout()
        master_hbox.addWidget(self.selector)
        self.setLayout(master_hbox)
