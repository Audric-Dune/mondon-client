# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt5.Qt import Qt, QPoint, pyqtSignal, QPixmap
from PyQt5.QtGui import QPainter, QColor, QPen

from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.image import Image
from commun.constants.colors import color_blanc, color_vert_moyen, color_gris_moyen
from commun.constants.dimensions import dict_width_selector_bobine,\
    dict_width_selector_refente,\
    dict_width_selector_poly
from commun.constants.stylesheets import black_14_label_stylesheet,\
    button_no_radius_stylesheet,\
    button_no_radius_orange_stylesheet,\
    green_14_label_stylesheet,\
    button_14_stylesheet
from gestion.stores.filter_store import filter_store


class SelectorCollumFilter(MondonWidget):

    def __init__(self, parent, title, name_filter, sort_mode, filter_mode):
        super(SelectorCollumFilter, self).__init__(parent)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFixedHeight(21)
        self.init_width(name_filter)
        self.set_background_color(color_blanc)
        self.sort_mode = sort_mode
        self.filter_mode = filter_mode
        self.title = title
        self.name_filter = name_filter
        self.filter_modal = None
        self.memo_filter_modal = False
        self.icon_sorted = QLabel()
        self.open_filter = QLabel()
        self.icon_sorted.setScaledContents(True)
        self.open_filter.setScaledContents(True)
        self.icon_sorted.setFixedSize(14, 14)
        self.open_filter.setFixedSize(14, 14)
        self.init_widget()
        self.update_widget()

    def init_width(self, name_filter):
        if filter_store.data_type == "bobine":
            width = dict_width_selector_bobine[name_filter]
            self.setMinimumWidth(width)
        if filter_store.data_type == "refente":
            width = dict_width_selector_refente[name_filter]
            self.setMinimumWidth(width)
        if filter_store.data_type == "poly":
            width = dict_width_selector_poly[name_filter]
            self.setMinimumWidth(width)

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 2, 5, 0)
        hbox.setSpacing(0)
        hbox.addWidget(self.get_label(self.title), alignment=Qt.AlignCenter | Qt.AlignVCenter)
        hbox.addWidget(self.icon_sorted)
        if self.sort_mode or self.filter_mode:
            hbox.addWidget(self.open_filter)
        self.setLayout(hbox)

    def update_widget(self):
        if filter_store.is_filtered(self.name_filter):
            self.open_filter.setPixmap(QPixmap("commun/assets/images/icon_filter_orange.png"))
        else:
            self.open_filter.setPixmap(QPixmap("commun/assets/images/arrow_down_vert_fonce.png"))
        if filter_store.sort_name == self.name_filter:
            name_image = "icon_sort_asc_orange" if filter_store.sort_asc else "icon_sort_dsc_orange"
            image = "commun/assets/images/{}.png".format(name_image)
            self.icon_sorted.setPixmap(QPixmap(image))
            self.icon_sorted.show()
        else:
            self.icon_sorted.hide()
        if self.filter_modal:
            self.filter_modal.update_widget()

    def on_filter_changed(self):
        self.update_widget()

    @staticmethod
    def get_label(text):
        label = QLabel(text)
        label.setStyleSheet(black_14_label_stylesheet)
        return label

    def open_modal(self):
        if self.sort_mode or self.filter_mode:
            pos = self.mapToGlobal(QPoint(0, self.height()))
            if self.filter_modal is None:
                self.filter_modal = FilterModal(parent=self,
                                                title=self.title,
                                                name_filter=self.name_filter,
                                                pos=pos,
                                                sort_mode=self.sort_mode,
                                                filter_mode=self.filter_mode,
                                                width=self.width())
                self.filter_modal.WANT_TO_CLOSE_SIGNAL.connect(self.close_modal)

    def close_modal(self):
        if self.filter_modal:
            self.filter_modal.close()
            self.filter_modal = None

    def enterEvent(self, e):
        if self.filter_modal:
            self.memo_filter_modal = True

    def leaveEvent(self, e):
        self.memo_filter_modal = False

    def mouseReleaseEvent(self, e):
        if self.memo_filter_modal:
            self.memo_filter_modal = False
        else:
            self.open_modal()
            self.memo_filter_modal = True
        super(SelectorCollumFilter, self).mouseReleaseEvent(e)


class FilterModal(QWidget):
    WANT_TO_CLOSE_SIGNAL = pyqtSignal()

    def __init__(self, pos, width, title, sort_mode, filter_mode, name_filter, parent=None):
        super(FilterModal, self).__init__(parent=parent)
        self.setWindowFlags(Qt.SplashScreen)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFocus()
        self.vbox = QVBoxLayout()
        self.bt_sorted_asc = QPushButton("Trier A -> Z")
        self.bt_sorted_dsc = QPushButton("Trier Z -> A")
        self.title = title
        self.name_filter = name_filter
        self.sort_mode = sort_mode
        self.filter_mode = filter_mode
        self.list_fiter = filter_store.dicts_filter[self.name_filter]
        self.setFixedWidth(width)
        self.move(pos)
        self.init_widget()
        self.show()

    def init_widget(self):
        self.vbox.setSpacing(5)
        self.vbox.setContentsMargins(1, 5, 1, 5)
        if self.sort_mode:
            if filter_store.sort_name == self.name_filter:
                if filter_store.sort_asc:
                    self.bt_sorted_asc.setStyleSheet(button_no_radius_orange_stylesheet)
                    self.bt_sorted_dsc.setStyleSheet(button_no_radius_stylesheet)
                else:
                    self.bt_sorted_asc.setStyleSheet(button_no_radius_stylesheet)
                    self.bt_sorted_dsc.setStyleSheet(button_no_radius_orange_stylesheet)
            else:
                self.bt_sorted_asc.setStyleSheet(button_no_radius_stylesheet)
                self.bt_sorted_dsc.setStyleSheet(button_no_radius_stylesheet)
            self.bt_sorted_asc.clicked.connect(self.on_click_bt_sorted_asc)
            self.bt_sorted_dsc.clicked.connect(self.on_click_bt_sorted_dsc)
            self.vbox.addWidget(self.bt_sorted_asc)
            self.vbox.addWidget(self.bt_sorted_dsc)
        if self.sort_mode and self.filter_mode:
            hbar = MondonWidget()
            hbar.setFixedHeight(2)
            hbar.set_background_color(color_gris_moyen)
            self.vbox.addWidget(hbar)
        if self.filter_mode:
            for value in self.list_fiter.keys():
                text = value
                if self.name_filter == "code_perfo":
                    text = "Perfo. " + chr(96 + value).capitalize() if value != "Tous" else value
                self.vbox.addWidget(LineFilter(parent=None, value=value, text=text, name_filter=self.name_filter))
            bt_ok = QPushButton("OK")
            bt_ok.setFixedWidth(40)
            bt_ok.setStyleSheet(button_14_stylesheet)
            bt_ok.clicked.connect(self.on_click_bt_ok)
            hbox = QHBoxLayout()
            hbox.addWidget(bt_ok)
            self.vbox.addLayout(hbox)
        self.setLayout(self.vbox)

    def update_widget(self):
        items = (self.vbox.itemAt(i) for i in range(self.vbox.count()))
        for item in items:
            if item.widget() and item.widget().objectName() == "LineFilter":
                item.widget().update_widget()

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
        self.WANT_TO_CLOSE_SIGNAL.emit()

    def on_click_bt_sorted_asc(self):
        filter_store.set_sort_param(sort_name=self.name_filter, sort_asc=True)
        self.WANT_TO_CLOSE_SIGNAL.emit()

    def on_click_bt_sorted_dsc(self):
        filter_store.set_sort_param(sort_name=self.name_filter, sort_asc=False)
        self.WANT_TO_CLOSE_SIGNAL.emit()

    def focusOutEvent(self, e):
        self.WANT_TO_CLOSE_SIGNAL.emit()


class LineFilter(MondonWidget):

    def __init__(self, parent, name_filter, value, text):
        super(LineFilter, self).__init__(parent=parent)
        self.set_background_color(color_blanc)
        self.setObjectName("LineFilter")
        self.setFocusPolicy(Qt.NoFocus)
        self.name_filter = name_filter
        self.value = value
        self.text = int(text) if isinstance(text, float) else text
        self.label = QLabel(str(self.text))
        self.check_icon = Image(parent=self, img="commun/assets/images/green_check.png", size=14)
        self.update_widget()
        self.init_widget()

    def update_widget(self):
        if filter_store.get_is_selected(self.name_filter, self.value):
            self.check_icon.show()
        else:
            self.check_icon.hide()

    def init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(5, 0, 5, 0)
        self.label.setStyleSheet(black_14_label_stylesheet)
        hbox.addWidget(self.label)
        hbox.addWidget(self.check_icon)
        self.setLayout(hbox)

    def mouseReleaseEvent(self, e):
        filter_store.set_is_selected(self.name_filter, self.value)
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
