# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import QEvent, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.Qt import Qt

from constants.colors import color_gris_fonce, color_vert_fonce

from ui.utils.drawing import draw_rectangle


class Dropdown(QWidget):
    def __init__(self, parent=None):
        super(Dropdown, self).__init__(parent=parent)
        self.installEventFilter(self)
        self.hbox = QHBoxLayout(self)
        self.label_dropdown = QLabel()
        self.popup = DropdownPopup()
        self.popup.hide()
        self.popup.POPUP_HIDE.connect(self.display_popup)
        self.popup.ITEM_CLICKED.connect(self.update_value_selected)
        self.show_popup = False
        self.list_popup_choice = []
        self.init_widget()

    def add_item(self, item_label):
        if self.popup:
            self.popup.add_item(item_label)

    def update_value_selected(self, value):
        self.label_dropdown.setText(value)

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonRelease:
            self.display_popup()
            return True
        return False

    def set_placeholder(self, placeholder=None):
        self.label_dropdown.setText(placeholder)

    def display_popup(self):
        if self.show_popup:
            self.popup.hide()
            self.show_popup = False
        else:
            pos_popup = self.mapToGlobal(QPoint(0, self.height()))
            self.popup.move(pos_popup)
            self.popup.setFixedWidth(self.width())
            self.popup.show()
            self.show_popup = True

    def init_widget(self):
        self.hbox.addWidget(self.label_dropdown)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_gris_fonce)

    def draw(self, p):
        self.draw_fond(p)


class DropdownPopup(QWidget):
    POPUP_HIDE = pyqtSignal()
    ITEM_CLICKED = pyqtSignal(str)

    def __init__(self, parent=None):
        super(DropdownPopup, self).__init__(parent=parent)
        self.vbox = QVBoxLayout(self)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.installEventFilter(self)
        self.show()

    def add_item(self, item_label):
        item = PopupItem(item_label)
        item.ITEM_CLICKED.connect(self.item_clicked)
        self.vbox.addWidget(item)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)
        self.setLayout(self.vbox)

    def item_clicked(self, text):
        self.ITEM_CLICKED.emit(text)
        self.POPUP_HIDE.emit()

    def eventFilter(self, object, event):
        if event.type() == QEvent.WindowDeactivate:
            self.POPUP_HIDE.emit()
            return True
        return False


class PopupItem(QWidget):
    ITEM_CLICKED = pyqtSignal(str)

    def __init__(self, item_label, parent=None):
        super(PopupItem, self).__init__(parent=parent)
        self.item_label = item_label
        self.init_label(item_label)
        self.hover = False
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QEvent.Enter:
            self.hover = True
            self.update()
            return True
        if event.type() == QEvent.Leave:
            self.hover = False
            self.update()
            return True
        if event.type() == QEvent.MouseButtonRelease:
            self.ITEM_CLICKED.emit(self.item_label)
            return True
        return False

    def init_label(self, text):
        label = QLabel(text)
        label.setFixedHeight(30)
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(label)
        self.setLayout(hbox)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        color = color_vert_fonce if self.hover else color_gris_fonce
        draw_rectangle(p, 0, 0, self.width(), self.height(), color)

    def draw(self, p):
        self.draw_fond(p)
