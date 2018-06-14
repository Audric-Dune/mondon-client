# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPen, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt

from commun.constants.colors import color_noir, color_blanc, color_vert_fonce, color_vert_moyen
from commun.constants.stylesheets import black_12_label_stylesheet,\
    white_12_no_bg_label_stylesheet,\
    gray_clair_12_no_bg_label_stylesheet


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
                                  icon_hover="commun/assets/images/edit_hover.png")
        self.bt_insert = ButtonMenu(parent=self, text="Insérer",
                                    icon="commun/assets/images/insert.png",
                                    icon_disabled="commun/assets/images/insert_disabled.png",
                                    icon_hover="commun/assets/images/insert_hover.png")
        self.bt_delete = ButtonMenu(parent=self, text="Supprimer",
                                    icon="commun/assets/images/delete.png",
                                    icon_disabled="commun/assets/images/delete_disabled.png",
                                    icon_hover="commun/assets/images/delete_hover.png")
        self.init_bt()
        self.init_ui()

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

    def init_bt(self):
        self.bt_edit.set_disabled(True)
        # BOUTON AJOUTER
        # self.bt_add.set_drop_down()
        # self.bt_add.add_item_drop_down(name="plan_prod", literral_name="Plan de production")
        # self.bt_add.add_item_drop_down(name="clean", literral_name="Nettoyage machine")
        # self.bt_add.add_item_drop_down(name="tool", literral_name="Action de maintenance")
        # self.bt_add.add_item_drop_down(name="stop", literral_name="Arrêt production")
        # self.bt_add.SELECT_ITEM.connect(self._handle_select_item_from_add)
        pass

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

    def _handle_select_item_from_add(self, item_selected_name):
        print("_handle_select_item_from_add")
        pass


class ButtonMenu(QWidget):

    def __init__(self, text, icon, icon_disabled, icon_hover, parent=None):
        super(ButtonMenu, self).__init__(parent=parent)
        self.setFixedWidth(70)
        self.label = QLabel(text)
        self.pixmap_icon = QLabel()
        self.pixmap_icon.setFixedSize(30, 30)
        self.icon = QPixmap(icon)
        self.icon_disabled = QPixmap(icon_disabled)
        self.icon_hover = QPixmap(icon_hover)
        self.background_color = color_blanc
        self.hover = False
        self.button_press = False
        self.disabled = False
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()
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
        if self.disabled:
            self.background_color = color_blanc
            self.pixmap_icon.setPixmap(self.icon_disabled)
            self.label.setStyleSheet(gray_clair_12_no_bg_label_stylesheet)
        elif self.button_press:
            self.background_color = color_vert_moyen
            self.pixmap_icon.setPixmap(self.icon_hover)
            self.label.setStyleSheet(white_12_no_bg_label_stylesheet)
        elif self.hover:
            self.background_color = color_vert_fonce
            self.pixmap_icon.setPixmap(self.icon_hover)
            self.label.setStyleSheet(white_12_no_bg_label_stylesheet)
        else:
            self.background_color = color_blanc
            self.pixmap_icon.setPixmap(self.icon)
            self.label.setStyleSheet(black_12_label_stylesheet)
        self.update()

    def set_disabled(self, p_bool):
        self.disabled = p_bool
        self.update_ui()

    def enterEvent(self, e):
        self.hover = True
        self.update_ui()
        super(ButtonMenu, self).enterEvent(e)

    def leaveEvent(self, e):
        self.hover = False
        self.update_ui()
        super(ButtonMenu, self).enterEvent(e)

    def mousePressEvent(self, e):
        self.button_press = True
        self.update_ui()
        super(ButtonMenu, self).enterEvent(e)

    def mouseReleaseEvent(self, e):
        self.button_press = False
        self.update_ui()
        super(ButtonMenu, self).enterEvent(e)
