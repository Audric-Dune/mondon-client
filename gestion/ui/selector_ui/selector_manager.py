# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QDesktopWidget
from gestion.ui.selector_ui.selector import Selector

from gestion.stores.filter_store import filter_store
from gestion.ui.selector_ui.selector_filter import SelectorFilter


class SelectorManager(QWidget):

    def __init__(self, plan_prod, parent):
        super(SelectorManager, self).__init__(parent=parent)
        self.setWindowFlags(Qt.Window)
        self.keyboardGrabber()
        self.vbox = QVBoxLayout()
        self.search_code = None
        self.selector = Selector(parent=self, plan_prod=plan_prod)
        filter_store.ON_DATA_TYPE_CHANGED.connect(self.on_data_type_changed)
        self.init_widget()

    def move_on_center(self):
        window_rect = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        window_rect.moveCenter(center_point)
        self.move(window_rect.topLeft())

    def init_widget(self):
        self.vbox.setContentsMargins(5, 5, 5, 5)
        self.vbox.setSpacing(10)
        self.setLayout(self.vbox)

    def on_data_type_changed(self):
        items = (self.vbox.itemAt(i) for i in range(self.vbox.count()))
        index = 0
        for item in items:
            if item and item.widget().objectName() == "SelectorFilter":
                self.vbox.takeAt(index).widget().deleteLater()
            index += 1
        selector_filter = SelectorFilter(parent=self)
        self.vbox.addWidget(selector_filter)
        self.vbox.addWidget(self.selector)

    def show(self):
        super(SelectorManager, self).show()
        self.move_on_center()

    def keyPressEvent(self, e):
        super(SelectorManager, self).keyPressEvent(e)
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, e):
        self.hide()
