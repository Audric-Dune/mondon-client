# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton


class SelectorPose(QMainWindow):
    def __init__(self, handle_selected_bobine, bobine):
        super(SelectorPose, self).__init__(None)
        self.bobine = bobine
        self.handle_selected_bobine = handle_selected_bobine
        self.poses = bobine.poses
        self.init_widget()

    def init_widget(self):
        central_widget = QWidget(self)
        hbox = QHBoxLayout()
        for pose in self.poses:
            self.add_bt_pose(hbox, pose, self.handle_bt_click)

        central_widget.setLayout(hbox)
        self.setCentralWidget(central_widget)

    @staticmethod
    def add_bt_pose(layout, pose, on_click):
        bt = QPushButton(str(pose))
        bt.clicked.connect(lambda: on_click(pose))
        layout.addWidget(bt)

    def handle_bt_click(self, pose):
        self.handle_selected_bobine(self.bobine, pose)
        self.close()

