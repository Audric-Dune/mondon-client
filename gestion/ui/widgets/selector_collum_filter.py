# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt5.Qt import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QCursor

from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.pixmap_button import PixmapButton
from commun.ui.public.image import Image
from commun.constants.colors import color_blanc, color_vert_moyen, color_gris_moyen
from commun.constants.stylesheets import black_14_label_stylesheet,\
    button_no_radius_no_hover_stylesheet,\
    button_no_radius_stylesheet,\
    green_14_label_stylesheet,\
    button_14_stylesheet
from gestion.stores.filter_store import filter_store


class SelectorCollumFilter(MondonWidget):

    def __init__(self, parent, set_filter_callback):
        super(SelectorCollumFilter, self).__init__(parent)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFixedHeight(21)
        self.set_background_color(color_blanc)
        self.set_filter_callback = set_filter_callback
        self.title = "Laize"
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
                                            title=self.title,
                                            pos=pos,
                                            width=self.width(),
                                            set_filter_callback=self.set_filter_callback)
            self.filter_modal.ON_CLOSE_SIGNAL.connect(self.on_close_modal)

    def on_close_modal(self):
        print("on_close_modal")
        if self.filter_modal:
            self.filter_modal.close()
            self.filter_modal = None

    def focusInEvent(self, e):
        cursor = QCursor()
        pos_cursor_from_widget = self.mapFromGlobal(cursor.pos())
        if self.childrenRect().contains(pos_cursor_from_widget):
            pass
        else:
            self.on_close_modal()
        super(SelectorCollumFilter, self).focusInEvent(e)

    def mouseReleaseEvent(self, e):
        self.bt_open_filter.click()
        super(SelectorCollumFilter, self).mouseReleaseEvent(e)


class FilterModal(QWidget):
    ON_CLOSE_SIGNAL = pyqtSignal()

    def __init__(self, pos, width, set_filter_callback, title, parent=None):
        super(FilterModal, self).__init__(parent=parent)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFocus()
        self.title = title
        self.set_filter_callback = set_filter_callback
        self.list_fiter = filter_store.dict_filter[self.title]
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
        for value in self.list_fiter.keys():
            vbox.addWidget(LineFilter(parent=None, value=value, title=self.title))
        bt_ok = QPushButton("OK")
        bt_ok.setFixedWidth(40)
        bt_ok.setStyleSheet(button_14_stylesheet)
        bt_ok.clicked.connect(self.on_click_bt_ok)
        hbox = QHBoxLayout()
        hbox.addWidget(bt_ok)
        vbox.addLayout(hbox)
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

    def on_click_bt_ok(self):
        self.ON_CLOSE_SIGNAL.emit()

    def on_click_bt_sorted_asc(self):
        self.set_filter_callback(sort_name="laize", sort_asc=True)
        self.ON_CLOSE_SIGNAL.emit()

    def on_click_bt_sorted_dsc(self):
        self.set_filter_callback(sort_name="laize", sort_asc=False)
        self.ON_CLOSE_SIGNAL.emit()


class LineFilter(MondonWidget):

    def __init__(self, parent, title, value):
        super(LineFilter, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.title = title
        self.value = value
        self.label = QLabel(str(int(value)))
        self.check_icon = Image(parent=self, img="commun/assets/images/green_check.png", size=14)
        self.update_widget()
        self.init_widget()

    def update_widget(self):
        if filter_store.get_is_selected(self.title, self.value):
            self.check_icon.show()
        else:
            self.check_icon.hide()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(5, 0, 5, 0)
        self.label.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(self.label)
        hbox.addStretch()
        hbox.addWidget(self.check_icon)
        self.setLayout(hbox)

    def mouseReleaseEvent(self, e):
        filter_store.set_is_selected(self.title, self.value)
        self.update_widget()
        super(LineFilter, self).mouseReleaseEvent(e)

    def enterEvent(self, e):
        self.set_background_color(color_vert_moyen)
        self.check_icon.add_image("commun/assets/images/white_check.png")
        self.label.setStyleSheet(green_14_label_stylesheet)
        super(LineFilter, self).enterEvent(e)

    def leaveEvent(self, e):
        self.set_background_color(color_blanc)
        self.check_icon.add_image("commun/assets/images/green_check.png")
        self.label.setStyleSheet(black_14_label_stylesheet)
        super(LineFilter, self).leaveEvent(e)
