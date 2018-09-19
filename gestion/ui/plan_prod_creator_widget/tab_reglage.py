# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPen, QPainter, QColor

from commun.constants.colors import color_noir, color_blanc, color_bleu_gris
from commun.constants.stylesheets import check_box_stylesheet_2,\
    black_14_label_stylesheet,\
    black_14_bold_label_stylesheet,\
    white_16_bold_label_stylesheet
from commun.ui.public.checkbox_button import CheckboxButton
from commun.utils.layout import clear_layout
from gestion.stores.settings_store import settings_store_gestion


class TabReglage(QWidget):

    def __init__(self, parent=None, plan_prod=None):
        super(TabReglage, self).__init__(parent=parent)
        self.plan_prod = plan_prod
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(20)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.init_ui()
        self.update_widget()

    def init_ui(self):
        self.setLayout(self.vbox)

    def update_widget(self):
        self.plan_prod.data_reglages.update_reglage()
        clear_layout(self.vbox)
        self.vbox.addWidget(LineMasterTitle(parent=self))
        # Bloc Préparation Production
        vbox_prepa = QVBoxLayout()
        vbox_prepa.setSpacing(2)
        vbox_prepa.addWidget(LineTitle(parent=self, text="Préparation production"))
        for data_reglage in self.plan_prod.data_reglages.data_reglages:
            if not data_reglage.reglage.is_optionnel() and data_reglage.reglage.cat != "CHAUFFE":
                vbox_prepa.addWidget(LineReglage(parent=self, data_reglage=data_reglage))
        self.vbox.addLayout(vbox_prepa)
        # Bloc Préparation Optionnelle
        vbox_option = QVBoxLayout()
        vbox_option.setSpacing(2)
        vbox_option.addWidget(LineTitle(parent=self, text="Préparation optionnelle"))
        for data_reglage in self.plan_prod.data_reglages.data_reglages:
            if data_reglage.reglage.is_optionnel():
                vbox_option.addWidget(LineReglage(parent=self, data_reglage=data_reglage))
        self.vbox.addLayout(vbox_option)
        # Bloc Temps de Réglage
        vbox_time = QVBoxLayout()
        vbox_time.setSpacing(2)
        vbox_time.addWidget(LineTitle(parent=self, text="Temps de préparation"))
        vbox_time.addWidget(LineTime(parent=self, text="Temps de préparation de l'aide conducteur (AC)",
                                     time=self.plan_prod.data_reglages.time_aide))
        vbox_time.addWidget(LineTime(parent=self, text="Temps de préparation du conducteur (C)",
                                     time=self.plan_prod.data_reglages.time_conducteur))
        for data_reglage in self.plan_prod.data_reglages.data_reglages:
            if not data_reglage.reglage.is_optionnel() and data_reglage.reglage.cat == "CHAUFFE":
                vbox_time.addWidget(LineTime(parent=self, text=data_reglage.reglage.des,
                                             time=data_reglage.reglage.time))
        self.vbox.addLayout(vbox_time)
        self.vbox.addStretch(0)


class LineTime(QWidget):

    def __init__(self, parent, time, text):
        super(LineTime, self).__init__(parent=parent)
        self.time = time
        self.text = text
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(4, 4, 4, 4)
        hbox.addWidget(self.create_label(text=self.text, align=Qt.AlignLeft | Qt.AlignVCenter))
        hbox.addWidget(self.create_label(text=self.time, width=100, time_format=True))
        self.setLayout(hbox)

    @staticmethod
    def create_label(text, width=None, stylesheet=black_14_label_stylesheet,
                     time_format=False, align=Qt.AlignCenter | Qt.AlignVCenter):
        import time
        text = time.strftime("%H:%M:%S", time.gmtime(text*60)) if time_format else text
        l = QLabel(text)
        if width:
            l.setFixedWidth(width)
        l.setStyleSheet(stylesheet)
        l.setAlignment(align)
        return l

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        color = color_blanc.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        p.fillRect(0, 0, self.width(), self.height(), qcolor)
        p.drawRect(0, 0, self.width()-1, self.height()-1)


class LineMasterTitle(QWidget):

    def __init__(self, parent):
        super(LineMasterTitle, self).__init__(parent)
        self.setFixedHeight(50)
        self.hbox = QHBoxLayout()
        title = QLabel("PREPARATION PRODUCTION")
        title.setStyleSheet(white_16_bold_label_stylesheet)
        title.setAlignment(Qt.AlignCenter)
        self.hbox.addWidget(title)
        self.setLayout(self.hbox)

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_bleu_gris.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        p.fillRect(0, 0, self.width(), self.height(), qcolor)


class LineTitle(QWidget):

    def __init__(self, parent, text):
        super(LineTitle, self).__init__(parent)
        self.hbox = QHBoxLayout()
        title = QLabel(text)
        title.setStyleSheet(black_14_bold_label_stylesheet)
        self.hbox.addWidget(title)
        self.setLayout(self.hbox)

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        color = color_blanc.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        p.fillRect(0, 0, self.width(), self.height(), qcolor)
        p.drawRect(0, 0, self.width()-1, self.height()-1)


class LineReglage(QWidget):

    def __init__(self, parent=None, data_reglage=None, reglage=None):
        super(LineReglage, self).__init__(parent=parent)
        self.data_reglage = data_reglage
        self.reglage = data_reglage.reglage if data_reglage else reglage
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(4, 4, 4, 4)
        hbox.addWidget(self.create_label("{} ({}min)".format(self.reglage.des, self.reglage.time),
                                         width=450, align=Qt.AlignLeft | Qt.AlignVCenter))
        qty = self.reglage.qty
        hbox.addWidget(self.create_label(text="x{}".format(qty)))
        hbox.addWidget(self.create_label(text="C", align=Qt.AlignRight | Qt.AlignVCenter))
        check_box_conducteur = CheckboxButton(parent=self,
                                              is_check=not self.data_reglage.check_box_conducteur,
                                              off_stylesheet=check_box_stylesheet_2,
                                              on_stylesheet=check_box_stylesheet_2,
                                              img_path="commun/assets/images/green_cross.png")
        check_box_conducteur.ON_CLICK_SIGNAL.connect(lambda: self.data_reglage.flip_check_box("conducteur"))
        check_box_conducteur.ON_CLICK_SIGNAL.connect(settings_store_gestion.on_data_reglage_changed)
        check_box_conducteur.setFixedSize(20, 20)
        hbox.addWidget(check_box_conducteur)
        hbox.addWidget(self.get_time_label(conducteur=True))
        hbox.addWidget(self.create_label(text="AC"))
        check_box_aide = CheckboxButton(parent=self,
                                        is_check=not self.data_reglage.check_box_aide,
                                        off_stylesheet=check_box_stylesheet_2,
                                        on_stylesheet=check_box_stylesheet_2,
                                        img_path="commun/assets/images/green_cross.png")
        check_box_aide.ON_CLICK_SIGNAL.connect(lambda: self.data_reglage.flip_check_box("aide"))
        check_box_aide.ON_CLICK_SIGNAL.connect(settings_store_gestion.on_data_reglage_changed)
        check_box_aide.setFixedSize(20, 20)
        hbox.addWidget(check_box_aide)
        hbox.addWidget(self.get_time_label(aide=True))
        self.setLayout(hbox)

    def get_time_label(self, conducteur=False, aide=False):
        if not self.data_reglage.check_box_conducteur and not self.data_reglage.check_box_aide:
            return self.create_label(text=0, time_format=True)
        if self.data_reglage.check_box_conducteur and self.data_reglage.check_box_aide:
            return self.create_label(text=self.data_reglage.reglage.time*self.data_reglage.reglage.qty/2,
                                     time_format=True)
        if self.data_reglage.check_box_conducteur and conducteur:
            return self.create_label(text=self.data_reglage.reglage.time*self.data_reglage.reglage.qty,
                                     time_format=True)
        if not self.data_reglage.check_box_conducteur and conducteur:
            return self.create_label(text=0, time_format=True)
        if self.data_reglage.check_box_aide and aide:
            return self.create_label(text=self.data_reglage.reglage.time*self.data_reglage.reglage.qty,
                                     time_format=True)
        if not self.data_reglage.check_box_aide and aide:
            return self.create_label(text=0, time_format=True)
        return QLabel()

    @staticmethod
    def create_label(text, width=None, stylesheet=black_14_label_stylesheet,
                     time_format=False, align=Qt.AlignCenter | Qt.AlignVCenter):
        import time
        text = time.strftime("%M:%S", time.gmtime(text*60)) if time_format else text
        l = QLabel(text)
        if width:
            l.setFixedWidth(width)
        l.setStyleSheet(stylesheet)
        l.setAlignment(align)
        return l

    def paintEvent(self, e):
        p = QPainter(self)
        color = color_noir.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        pen = QPen()
        pen.setColor(qcolor)
        p.setPen(pen)
        color = color_blanc.rgb_components
        qcolor = QColor(color[0], color[1], color[2])
        p.fillRect(0, 0, self.width(), self.height(), qcolor)
        p.drawRect(0, 0, self.width()-1, self.height()-1)
