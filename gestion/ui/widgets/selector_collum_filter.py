# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt5.Qt import Qt, QPoint, QEvent, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen

from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.pixmap_button import PixmapButton
from commun.ui.public.image import Image
from commun.constants.colors import color_blanc, color_vert_moyen, color_gris_moyen
from commun.constants.stylesheets import black_14_label_stylesheet,\
    button_no_radius_no_hover_stylesheet,\
    button_no_radius_stylesheet,\
    green_14_label_stylesheet


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
        if self.filter_modal:
            self.filter_modal.close()
            self.filter_modal = None
        else:
            pos = self.mapToGlobal(QPoint(0, self.height()))
            self.filter_modal = FilterModal(parent=self,
                                            pos=pos,
                                            width=self.width(),
                                            set_filter_callback=self.set_filter_callback)
            self.filter_modal.ON_CLOSE_SIGNAL.connect(self.on_close_modal)
            self.filter_modal.ON_FOCUS_OUT_SIGNAL.connect(lambda: self.on_close_modal(kill=False))

    def on_close_modal(self, kill=True):
        if self.filter_modal:
            self.filter_modal.close()
            if kill:
                self.filter_modal = None

    def eventFilter(self, o, e):
        if e.type() == QEvent.MouseButtonRelease:
            self.bt_open_filter.click()
            return True
        return False


class FilterModal(QWidget):
    ON_CLOSE_SIGNAL = pyqtSignal
    ON_FOCUS_OUT_SIGNAL = pyqtSignal

    def __init__(self, pos, width, set_filter_callback, parent=None):
        super(FilterModal, self).__init__(parent=parent)
        self.setFocusPolicy(Qt.ClickFocus)
        self.set_filter_callback = set_filter_callback
        self.list_fiter = [(130, True), (140, True), (150, False)]
        self.setWindowFlags(Qt.SplashScreen)
        self.setFixedWidth(width)
        self.move(pos)
        self.init_widget()
        self.show()

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(5)
        vbox.setContentsMargins(1, 5, 1, 5)
        bt_sorted_asc = QPushButton("Trier A -> Z")
        bt_sorted_asc.setStyleSheet(button_no_radius_stylesheet)
        bt_sorted_asc.clicked.connect(self.on_click_bt_sorted_asc)
        bt_sorted_dsc = QPushButton("Trier Z -> A")
        bt_sorted_dsc.setStyleSheet(button_no_radius_stylesheet)
        bt_sorted_dsc.clicked.connect(self.on_click_bt_sorted_dsc)
        vbox.addWidget(bt_sorted_asc)
        vbox.addWidget(bt_sorted_dsc)
        for value in self.list_fiter:
            vbox.addWidget(LineFilter(parent=None, value=value[0], selected=value[1]))
        self.setLayout(vbox)

    def paintEvent(self, event):
        p = QPainter(self)
        color = color_blanc.rgb_components
        qcolor_blanc = QColor(color[0], color[1], color[2])
        color = color_gris_moyen.rgb_components
        qcolor_gris = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor_gris)
        p.setPen(pen)
        p.fillRect(0, 0, self.width(), self.height(), qcolor_blanc)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    def on_click_bt_sorted_asc(self):
        self.set_filter_callback(sort_name="laize", sort_asc=True)
        self.ON_CLOSE_SIGNAL.emit()

    def on_click_bt_sorted_dsc(self):
        self.set_filter_callback(sort_name="laize", sort_asc=False)
        self.ON_CLOSE_SIGNAL.emit()

    def closeEvent(self, e):
        self.ON_CLOSE_SIGNAL.emit()
        super(FilterModal, self).focusInEvent(e)

    def focusOutEvent(self, e):
        self.ON_FOCUS_OUT_SIGNAL.emit()
        super(FilterModal, self).focusOutEvent(e)


class LineFilter(MondonWidget):

    def __init__(self, parent, value, selected):
        super(LineFilter, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.installEventFilter(self)
        self.label = QLabel(str(value))
        self.check_icon = Image(parent=self, img="commun/assets/images/green_check.png", size=14)
        if not selected:
            self.check_icon.hide()
        self.selected = selected
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(5, 0, 5, 0)
        self.label.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(self.label)
        hbox.addStretch()
        hbox.addWidget(self.check_icon)
        self.setLayout(hbox)

    def eventFilter(self, o, e):
        if e.type() == QEvent.Enter:
            self.set_background_color(color_vert_moyen)
            self.check_icon.add_image("commun/assets/images/white_check.png")
            self.label.setStyleSheet(green_14_label_stylesheet)
            return True
        if e.type() == QEvent.Leave:
            self.set_background_color(color_blanc)
            self.check_icon.add_image("commun/assets/images/green_check.png")
            self.label.setStyleSheet(black_14_label_stylesheet)
            return True
        return False
