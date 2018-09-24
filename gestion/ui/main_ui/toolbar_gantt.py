# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPen, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

from commun.constants.colors import color_noir, color_blanc, color_vert_fonce, color_vert_moyen,\
    color_gris_moyen, color_rouge, color_rouge_clair
from commun.constants.stylesheets import black_12_label_stylesheet,\
    white_12_no_bg_label_stylesheet, \
    gray_moyen_12_no_bg_label_stylesheet

from gestion.stores.settings_store import settings_store_gestion


class ToolbarGantt(QWidget):

    def __init__(self, parent=None):
        super(ToolbarGantt, self).__init__(parent=parent)
        self.bt_add = ButtonMenu(parent=self, text="Ajouter",
                                 icon="commun/assets/images/add.png",
                                 icon_disabled="commun/assets/images/add_disabled.png",
                                 icon_hover="commun/assets/images/add_hover.png")
        self.bt_edit = ButtonMenu(parent=self, text="Editer",
                                  icon="commun/assets/images/edit.png",
                                  icon_disabled="commun/assets/images/edit_disabled.png",
                                  icon_hover="commun/assets/images/edit_hover.png",
                                  callback=self._handle_select_item_from_edit)
        self.bt_insert = ButtonMenu(parent=self, text="Insérer",
                                    icon="commun/assets/images/insert.png",
                                    icon_disabled="commun/assets/images/insert_disabled.png",
                                    icon_hover="commun/assets/images/insert_hover.png",
                                    callback=self._handle_select_item_from_insert)
        self.bt_delete = ButtonMenu(parent=self, text="Supprimer",
                                    icon="commun/assets/images/delete.png",
                                    icon_disabled="commun/assets/images/delete_disabled.png",
                                    icon_hover="commun/assets/images/delete_hover.png",
                                    callback=self._handle_click_bt_delete,
                                    risk_style=True)
        settings_store_gestion.FOCUS_CHANGED_SIGNAL.connect(self.update_ui)
        settings_store_gestion.ON_DAY_CHANGED.connect(self.update_ui)
        self.init_bt()
        self.init_ui()
        self.update_ui()

    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addWidget(self.bt_add)
        hbox.addWidget(self.bt_edit)
        hbox.addWidget(self.bt_insert)
        hbox.addWidget(self.bt_delete)
        hbox.addStretch()
        self.setLayout(hbox)

    def update_ui(self):
        if settings_store_gestion.day_ago > 0:
            self.bt_add.set_disabled(True)
        else:
            self.bt_add.set_disabled(False)
        if settings_store_gestion.focus:
            self.bt_insert.set_disabled(False)
            self.bt_delete.set_disabled(False)
            self.bt_edit.set_disabled(False)
        else:
            self.bt_insert.set_disabled(True)
            self.bt_delete.set_disabled(True)
            self.bt_edit.set_disabled(True)
        if settings_store_gestion.standing_insert:
            self.bt_insert.set_disabled(True)
        self.bt_delete.update_ui()
        self.bt_edit.update_ui()

    def init_bt(self):
        self.bt_add.set_dropdown(callback=self._handle_select_item_from_add)
        self.bt_add.add_item_drop_down(name="plan_prod", literral_name="Plan de production")
        self.bt_add.add_item_drop_down(name="clean", literral_name="Nettoyage machine")
        self.bt_add.add_item_drop_down(name="tool", literral_name="Action de maintenance")
        self.bt_add.add_item_drop_down(name="stop", literral_name="Arrêt production")

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.drawRect(0, 0, self.width()-1, self.height()-1)
        color = color_blanc.rgb_components
        qcolor_background = QColor(color[0], color[1], color[2])
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(qcolor_background)
        p.setBrush(brush)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    @staticmethod
    def _handle_select_item_from_add(item_selected_name):
        if item_selected_name == "plan_prod":
            settings_store_gestion.create_new_plan()
        else:
            settings_store_gestion.create_new_event(item_selected_name)

    @staticmethod
    def _handle_select_item_from_edit():
        settings_store_gestion.focus_edit()

    @staticmethod
    def _handle_select_item_from_insert():
        settings_store_gestion.focus_insert()

    @staticmethod
    def _handle_click_bt_delete():
        settings_store_gestion.delete_item()


class ButtonMenu(QWidget):

    def __init__(self, text, icon, icon_disabled, icon_hover, parent=None, callback=None, risk_style=None):
        super(ButtonMenu, self).__init__(parent=parent)
        self.setFixedWidth(70)
        self.vbox = QVBoxLayout()
        self.label = QLabel(text)
        self.pixmap_icon = QLabel()
        self.pixmap_icon.setFixedSize(30, 30)
        self.icon = QPixmap(icon)
        self.icon_disabled = QPixmap(icon_disabled)
        self.icon_hover = QPixmap(icon_hover)
        self.risk_style = risk_style
        self.dropdown = None
        self.background_color = color_blanc
        self.hover = False
        self.button_press = False
        self.disabled = False
        self.popup_show = False
        self.callback = callback
        self.init_ui(self.vbox)

    def init_ui(self, vbox):
        vbox.setContentsMargins(0, 5, 0, 5)
        vbox.setSpacing(0)
        self.setLayout(vbox)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.pixmap_icon)
        self.pixmap_icon.setPixmap(self.icon)
        self.pixmap_icon.setScaledContents(True)
        self.pixmap_icon.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        vbox.addLayout(hbox)
        self.label.setStyleSheet(black_12_label_stylesheet)
        self.label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.label)
        self.setLayout(vbox)

    def paintEvent(self, e):
        p = QPainter(self)
        color = self.background_color.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.fillRect(1, 1, self.width()-2, self.height()-2, qcolor)

    def update_ui(self):
        if self.dropdown is not None:
            self.dropdown.update_ui()
        if self.popup_show:
            self.background_color = color_rouge_clair if self.risk_style else color_vert_moyen
            self.pixmap_icon.setPixmap(self.icon_hover)
            self.label.setStyleSheet(white_12_no_bg_label_stylesheet)
        elif self.disabled:
            self.background_color = color_blanc
            self.pixmap_icon.setPixmap(self.icon_disabled)
            self.label.setStyleSheet(gray_moyen_12_no_bg_label_stylesheet)
        elif self.button_press:
            self.background_color = color_rouge_clair if self.risk_style else color_vert_moyen
            self.pixmap_icon.setPixmap(self.icon_hover)
            self.label.setStyleSheet(white_12_no_bg_label_stylesheet)
        elif self.hover:
            self.background_color = color_rouge if self.risk_style else color_vert_moyen
            self.pixmap_icon.setPixmap(self.icon_hover)
            self.label.setStyleSheet(white_12_no_bg_label_stylesheet)
        else:
            self.background_color = color_blanc
            self.pixmap_icon.setPixmap(self.icon)
            self.label.setStyleSheet(black_12_label_stylesheet)
        self.update()

    def set_dropdown(self, callback):
        self.dropdown = DropDown(parent=self)
        self.dropdown.SELECT_ITEM_SIGNAL.connect(callback)
        self.vbox.addWidget(self.dropdown)

    def add_item_drop_down(self, name, literral_name):
        if self.dropdown is None:
            return
        self.dropdown.popup.add_item(name=name, literral_name=literral_name)

    def set_disabled(self, p_bool):
        self.disabled = p_bool
        self.update_ui()

    def _handle_button_press(self):
        if self.disabled:
            return
        if self.dropdown:
            self.dropdown.show_popup()
        elif self.callback is not None:
            self.callback()

    def enterEvent(self, e):
        self.hover = True
        self.update_ui()
        super(ButtonMenu, self).enterEvent(e)

    def leaveEvent(self, e):
        self.hover = False
        self.update_ui()
        super(ButtonMenu, self).enterEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.button_press = True
            self.update_ui()
        super(ButtonMenu, self).enterEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.button_press = False
            self._handle_button_press()
            self.update_ui()
        super(ButtonMenu, self).enterEvent(e)


class DropDown(QWidget):
    SELECT_ITEM_SIGNAL = pyqtSignal(str)

    def __init__(self, parent):
        super(DropDown, self).__init__(parent=parent)
        self.parent = parent
        self.hover = False
        self.button_press = False
        self.disabled = False
        self.popup_show = False
        self.background_color = color_blanc
        self.pixmap_icon = QLabel()
        self.pixmap_icon.setFixedSize(15, 15)
        self.icon = QPixmap("commun/assets/images/arrow.png")
        self.icon_disabled = QPixmap("commun/assets/images/arrow_disabled.png")
        self.icon_hover = QPixmap("commun/assets/images/arrow_hover.png")
        self.popup = Popup()
        self.popup.HIDE_SIGNAL.connect(self._handle_hide_popup)
        self.popup.SELECT_ITEM_SIGNAL.connect(self._handle_select_item)
        self.init_ui()
        self.update_ui()

    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        self.pixmap_icon.setAlignment(Qt.AlignCenter)
        self.pixmap_icon.setScaledContents(True)
        hbox.addWidget(self.pixmap_icon)
        self.setLayout(hbox)

    def update_ui(self):
        self.popup_show = self.parent.popup_show
        self.hover = self.parent.hover
        self.button_press = self.parent.button_press
        self.disabled = self.parent.disabled
        if self.popup_show:
            self.background_color = color_rouge_clair if self.parent.risk_style else color_vert_moyen
            self.pixmap_icon.setPixmap(self.icon_hover)
        elif self.disabled:
            self.background_color = color_blanc
            self.pixmap_icon.setPixmap(self.icon_disabled)
        elif self.button_press:
            self.background_color = color_rouge_clair if self.parent.risk_style else color_vert_moyen
            self.pixmap_icon.setPixmap(self.icon_hover)
        elif self.hover:
            self.background_color = color_rouge_clair if self.parent.risk_style else color_vert_fonce
            self.pixmap_icon.setPixmap(self.icon_hover)
        else:
            self.background_color = color_blanc
            self.pixmap_icon.setPixmap(self.icon)
        self.update()

    def _handle_hide_popup(self):
        self.parent.popup_show = False
        self.parent.update_ui()

    def _handle_select_item(self, name):
        self.SELECT_ITEM_SIGNAL.emit(name)

    def show_popup(self):
        pos_popup = self.mapToGlobal(QPoint(0, self.height()))
        self.popup.move(pos_popup)
        self.parent.popup_show = True
        self.parent.update_ui()
        self.popup.show()


class Popup(QWidget):
    SELECT_ITEM_SIGNAL = pyqtSignal(str)
    HIDE_SIGNAL = pyqtSignal()

    def __init__(self):
        super(Popup, self).__init__()
        self.setWindowFlags(Qt.Popup)
        self.vbox = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.vbox.setContentsMargins(1, 1, 1, 1)
        self.vbox.setSpacing(0)
        self.setLayout(self.vbox)

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_gris_moyen.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.drawRect(0, 0, self.width()-1, self.height()-1)

    def add_item(self, name, literral_name):
        new_line = LineItem(name=name)
        new_line.CLICKED_SIGNAL.connect(self._handle_select_item)
        new_line.setText(literral_name)
        self.vbox.addWidget(new_line)
        self.update()

    def _handle_select_item(self, name):
        self.SELECT_ITEM_SIGNAL.emit(name)
        self.hide()

    def hideEvent(self, e):
        self.HIDE_SIGNAL.emit()
        super(Popup, self).hideEvent(e)


class LineItem(QLabel):
    CLICKED_SIGNAL = pyqtSignal(str)

    def __init__(self, name):
        super(LineItem, self).__init__()
        self.name = name
        self.background_color = color_blanc
        self.setStyleSheet(black_12_label_stylesheet)
        self.setFixedHeight(30)

    def paintEvent(self, e):
        p = QPainter(self)
        color = self.background_color.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        p.fillRect(0, 0, self.width(), self.height(), qcolor)
        super(LineItem, self).paintEvent(e)

    def mousePressEvent(self, e):
        self.background_color = color_vert_moyen
        self.update()
        super(LineItem, self).mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.CLICKED_SIGNAL.emit(self.name)
        super(LineItem, self).mouseReleaseEvent(e)

    def enterEvent(self, e):
        self.setStyleSheet(white_12_no_bg_label_stylesheet)
        self.background_color = color_vert_fonce
        self.update()
        super(LineItem, self).enterEvent(e)

    def leaveEvent(self, e):
        self.setStyleSheet(black_12_label_stylesheet)
        self.background_color = color_blanc
        self.update()
        super(LineItem, self).enterEvent(e)
