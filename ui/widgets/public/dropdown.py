# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QEvent, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.Qt import Qt

from constants.colors import color_vert_fonce, color_blanc
from constants.stylesheets import black_16_label_stylesheet,\
    white_16_label_stylesheet,\
    button_arrow_stylesheet,\
    button_dropdown_stylesheet

from ui.utils.drawing import draw_rectangle


class Dropdown(QWidget):
    VALUE_SELECTED_SIGNAL = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Dropdown, self).__init__(parent=parent)
        self.hbox = QHBoxLayout(self)
        self.bt_dropdown = QPushButton(self)
        self.bt_dropdown.setStyleSheet(button_dropdown_stylesheet)
        self.bt_dropdown.clicked.connect(self.display_popup)
        self.bt_arrow_dropdown = QPushButton(self)
        self.bt_arrow_dropdown.setStyleSheet(button_arrow_stylesheet)
        self.bt_arrow_dropdown.clicked.connect(self.display_popup)
        img = QIcon("assets/images/arrow_down_vert_fonce.png")
        self.bt_arrow_dropdown.setIcon(img)
        self.placeholder = None
        self.activated = False
        self.popup = DropdownPopup()
        self.popup.hide()
        self.popup.POPUP_HIDE.connect(self.display_popup)
        self.popup.ITEM_CLICKED.connect(self.update_value_selected)
        self.show_popup = False
        self.init_widget()

    def add_item(self, item_label):
        if self.popup:
            self.popup.add_item(item_label)

    def update_value_selected(self, value):
        self.bt_dropdown.setText(value)
        self.VALUE_SELECTED_SIGNAL.emit(value)

    def set_activated(self, bool):
        self.update_widget(bool)

    def set_placeholder(self, placeholder=None):
        if placeholder:
            self.placeholder = placeholder
        self.bt_dropdown.setText(self.placeholder)

    def display_popup(self):
        if self.show_popup:
            self.popup.hide()
            self.show_popup = False
        else:
            pos_popup = self.mapToGlobal(QPoint(0, self.height()))
            self.popup.move(pos_popup)
            self.popup.setFixedWidth(self.width())
            self.popup.show()
            self.popup.show_popup = True
            self.show_popup = True

    def update_widget(self, bool):
        self.activated = bool
        if bool:
            self.bt_dropdown.setDisabled(False)
            self.bt_arrow_dropdown.setDisabled(False)
        else:
            self.bt_dropdown.setDisabled(True)
            self.bt_arrow_dropdown.setDisabled(True)
            self.set_placeholder()

    def init_widget(self):
        self.bt_dropdown.setFixedSize(250, 24)
        self.hbox.addWidget(self.bt_dropdown)
        self.bt_arrow_dropdown.setFixedSize(24, 24)
        self.hbox.addWidget(self.bt_arrow_dropdown)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        self.setLayout(self.hbox)


class DropdownPopup(QWidget):
    POPUP_HIDE = pyqtSignal()
    ITEM_CLICKED = pyqtSignal(str)

    def __init__(self, parent=None):
        super(DropdownPopup, self).__init__(parent=parent)
        self.vbox = QVBoxLayout(self)
        # self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.installEventFilter(self)
        self.show_popup = True
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
        if event.type() == QEvent.WindowDeactivate and self.show_popup:
            self.show_popup = False
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
            self.label.setStyleSheet(white_16_label_stylesheet)
            self.update()
            return True
        if event.type() == QEvent.Leave:
            self.hover = False
            self.label.setStyleSheet(black_16_label_stylesheet)
            self.update()
            return True
        if event.type() == QEvent.MouseButtonRelease:
            self.ITEM_CLICKED.emit(self.item_label)
            return True
        return False

    def init_label(self, text):
        self.label = QLabel(text)
        self.label.setFixedHeight(30)
        self.label.setStyleSheet(black_16_label_stylesheet)
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(5, 0, 0, 0)
        hbox.addWidget(self.label)
        self.setLayout(hbox)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        color = color_vert_fonce if self.hover else color_blanc
        draw_rectangle(p, 0, 0, self.width(), self.height(), color)

    def draw(self, p):
        self.draw_fond(p)
