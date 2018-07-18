# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

from commun.constants.stylesheets import button_stylesheet, white_16_bold_label_stylesheet, white_12_label_stylesheet
from commun.constants.colors import color_bleu_gris


class SelectorPose(QWidget):
    def __init__(self, handle_selected_bobine, bobine):
        super(SelectorPose, self).__init__(None)
        self.setWindowFlags(Qt.Dialog)
        self.bobine = bobine
        self.handle_selected_bobine = handle_selected_bobine
        self.poses = sorted(bobine.valid_poses)
        self.init_widget()

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(2, 2, 2, 2)
        vbox.addWidget(self.get_bloc_title())
        vbox.addWidget(self.get_bloc_info())
        vbox.addWidget(self.get_bloc_bt())
        self.setLayout(vbox)

    def get_bloc_title(self):
        title_contain = QWidget(parent=self)
        self.set_background_color(title_contain)
        title_label = QLabel(self.bobine.code)
        title_label.setStyleSheet(white_16_bold_label_stylesheet)
        title_contain_hbox = QHBoxLayout()
        title_contain_hbox.addWidget(title_label)
        title_contain.setLayout(title_contain_hbox)
        return title_contain

    def get_bloc_info(self):
        info_contain = QWidget(parent=self)
        self.set_background_color(info_contain)
        info_label = QLabel("Sélectionner le nombre de pistes:")
        info_label.setStyleSheet(white_12_label_stylesheet)
        info_contain_hbox = QHBoxLayout()
        info_contain_hbox.addWidget(info_label)
        info_contain.setLayout(info_contain_hbox)
        return info_contain

    def get_bloc_bt(self):
        bt_contain = QWidget(parent=self)
        self.set_background_color(bt_contain)
        hbox = QHBoxLayout()
        for pose in self.poses:
            self.add_bt_pose(hbox, pose, self.handle_bt_click)
        bt_contain.setLayout(hbox)
        return bt_contain

    @staticmethod
    def set_background_color(widget):
        widget.setStyleSheet(
            "background-color:{color_bleu_gris};".format(color_bleu_gris=color_bleu_gris.hex_string)
        )

    @staticmethod
    def add_bt_pose(layout, pose, on_click):
        bt = QPushButton(str(pose))
        bt.setStyleSheet(button_stylesheet)
        bt.clicked.connect(lambda: on_click(pose))
        layout.addWidget(bt)

    def handle_bt_click(self, pose):
        self.handle_selected_bobine(self.bobine, pose)
        self.close()

