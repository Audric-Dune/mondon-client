# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class SelectorPose(QWidget):
    def __init__(self, handle_selected_bobine, bobine):
        super(SelectorPose, self).__init__(None)
        self.setWindowFlags(Qt.Dialog)
        self.bobine = bobine
        self.handle_selected_bobine = handle_selected_bobine
        self.poses = bobine.poses
        self.init_widget()

    def init_widget(self):
        hbox = QHBoxLayout()
        for pose in self.poses:
            self.add_bt_pose(hbox, pose, self.handle_bt_click)

        self.setLayout(hbox)

    @staticmethod
    def add_bt_pose(layout, pose, on_click):
        bt = QPushButton(str(pose))
        bt.clicked.connect(lambda: on_click(pose))
        layout.addWidget(bt)

    def handle_bt_click(self, pose):
        self.handle_selected_bobine(self.bobine, pose)
        self.close()

