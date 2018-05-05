# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt5.Qt import Qt, QPoint, QEvent

from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.pixmap_button import PixmapButton
from commun.constants.colors import color_blanc
from commun.constants.stylesheets import black_14_label_stylesheet,\
    button_no_radius_no_hover_stylesheet,\
    button_no_radius_stylesheet


class SelectorCollumFilter(MondonWidget):

    def __init__(self, parent, set_filter_callback):
        super(SelectorCollumFilter, self).__init__(parent)
        self.installEventFilter(self)
        self.setFixedHeight(21)
        self.set_background_color(color_blanc)
        self.set_filter_callback = set_filter_callback
        self.title = "Laize"
        self.filter_list = [150, 140]
        self.filter_modal = None
        self.bt_open_filter = PixmapButton(parent=self)
        self.bt_open_filter.clicked.connect(self.on_click_bt_open_filter)
        self.init_bt(self.bt_open_filter)
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.get_label(self.title))
        hbox.addWidget(self.bt_open_filter)
        self.setLayout(hbox)

    def init_bt(self, bt):
        bt.addImage("commun/assets/images/arrow_down_vert_fonce.png")
        bt.setStyleSheet(button_no_radius_no_hover_stylesheet)
        bt.setFixedSize(self.height(), self.height())

    @staticmethod
    def get_label(text):
        label = QLabel(text)
        label.setStyleSheet(black_14_label_stylesheet)
        return label

    def on_click_bt_open_filter(self):
        pos = self.mapToGlobal(QPoint(0, self.height()))
        self.filter_modal = FilterModal(parent=self,
                                        pos=pos,
                                        width=self.width(),
                                        set_filter_callback=self.set_filter_callback)

    def eventFilter(self, o, e):
        if e.type() == QEvent.MouseButtonRelease:
            self.bt_open_filter.click()
            return True
        return False


class FilterModal(QWidget):

    def __init__(self, pos, width, set_filter_callback, parent=None):
        super(FilterModal, self).__init__(parent=parent)
        self.set_filter_callback = set_filter_callback
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setStyleSheet("background-color:{};".format(color_blanc.hex_string))
        self.setFixedWidth(width)
        self.move(pos)
        self.init_widget()
        self.show()

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(5)
        vbox.setContentsMargins(0, 5, 0, 5)
        bt_sorted_asc = QPushButton("Trier A -> Z")
        bt_sorted_asc.setStyleSheet(button_no_radius_stylesheet)
        bt_sorted_asc.clicked.connect(self.on_click_bt_sorted_asc)
        bt_sorted_dsc = QPushButton("Trier Z -> A")
        bt_sorted_dsc.setStyleSheet(button_no_radius_stylesheet)
        bt_sorted_dsc.clicked.connect(self.on_click_bt_sorted_dsc)
        vbox.addWidget(bt_sorted_asc)
        vbox.addWidget(bt_sorted_dsc)
        self.setLayout(vbox)

    def on_click_bt_sorted_asc(self):
        self.set_filter_callback(sort_name="laize", sort_asc=True)
        self.close()

    def on_click_bt_sorted_dsc(self):
        self.set_filter_callback(sort_name="laize", sort_asc=False)
        self.close()