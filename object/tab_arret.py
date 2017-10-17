# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation des module PyQt5
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QLabel, QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QRectF, QTimer, QSize
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QIcon
from param.param import *
from datetime import datetime, timedelta
from object.data_store_manager import *
from object.base_de_donnee import *
from object.stat_legend import StatLegend
from object.stat_bar import StatBar
from object.settings_store import *
from fonction.gestion_timestamp import *
from fonction.draw_fonction import draw_rectangle, draw_text, draw_rectangle_radius


class TabArret(QWidget):
    def __init__(self, parent, moment):
        super(TabArret, self).__init__(parent=parent)
        self.moment = moment
        self.day_ago = 0
        self.data = []
        self.labels_hours = []
        self.labels_time = []
        self.init_widgets()
        self.get_data()
        settings_store.add_listener(self.get_setting)
        data_store_manager.add_listener(self.update_new_data)

    def create_grid(self, index):
        grid = QGridLayout()
        grid.setSpacing(0)
        for line in range(5):
            label_index = QLabel(str(index + 1))
            label_index.setFixedWidth(40)
            label_index.setAlignment(Qt.AlignCenter)
            label_index.setStyleSheet(
                "QLabel {color: rgb(255, 255, 255); font-size: 14px; background-color: rgb(44, 62, 80)}")
            grid.addWidget(label_index, line, 0)
            self.labels_hours.append(QLabel())
            self.labels_hours[index].setAlignment(Qt.AlignCenter)
            self.labels_hours[index].setFixedWidth(80)
            self.labels_hours[index].setStyleSheet(
                "QLabel {color: rgb(255, 255, 255); font-size: 14px; background-color: rgb(44, 62, 80)}")
            grid.addWidget(self.labels_hours[index], line, 1)
            self.labels_time.append(QLabel())
            self.labels_time[index].setAlignment(Qt.AlignCenter)
            self.labels_time[index].setFixedWidth(80)
            self.labels_time[index].setStyleSheet(
                "QLabel {color: rgb(255, 255, 255); font-size: 14px; background-color: rgb(44, 62, 80)}")
            grid.addWidget(self.labels_time[index], line, 2)
            index += 1
        return grid

    def create_grid_title(self):
        grid = QGridLayout()
        grid.setSpacing(0)
        label_index = QLabel("Num")
        label_index.setFixedWidth(40)
        label_index.setAlignment(Qt.AlignCenter)
        label_index.setStyleSheet(
            "QLabel {color: rgb(255, 255, 255); font-size: 14px; background-color: rgb(44, 62, 80)}")
        grid.addWidget(label_index, 0, 0)
        labels_hours = QLabel("Heure")
        labels_hours.setAlignment(Qt.AlignCenter)
        labels_hours.setFixedWidth(80)
        labels_hours.setStyleSheet(
            "QLabel {color: rgb(255, 255, 255); font-size: 14px; background-color: rgb(44, 62, 80)}")
        grid.addWidget(labels_hours, 0, 1)
        labels_time = QLabel("Temps")
        labels_time.setAlignment(Qt.AlignCenter)
        labels_time.setFixedWidth(80)
        labels_time.setStyleSheet(
            "QLabel {color: rgb(255, 255, 255); font-size: 14px; background-color: rgb(44, 62, 80)}")
        grid.addWidget(labels_time, 0, 2)
        return grid

    def init_widgets(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addStretch()
        for i in range(3):
            vbox = QVBoxLayout()
            vbox.setContentsMargins(0, 0, 0, 0)
            title = self.create_grid_title()
            grid = self.create_grid(i*5)
            vbox.addLayout(title)
            vbox.addLayout(grid)
            hbox.addLayout(vbox)
            hbox.addStretch()
        self.setLayout(hbox)

    def get_data(self):
        speeds = data_store_manager.store.data
        ts = timestamp_at_day_ago(self.day_ago)

        vendredi = timestamp_to_day(ts) == "Vendredi"
        start = 6
        mid = 13 if vendredi else 14
        end = 20 if vendredi else 22

        if self.moment == "matin":
            end = mid
        if self.moment == "soir":
            start = mid

        start_ts = timestamp_at_time(ts, hours=start)
        end_ts = timestamp_at_time(ts, hours=end)

        speed_is_0 = False
        data = []
        start = 0
        end = 0
        for value in speeds:
            if start_ts <= value[0] < end_ts:
                if value == len(speeds):
                    data.append((start, end))
                if 0 <= value[1] <= 60:
                    if not speed_is_0:
                        start = value[0]
                    end = value[0]
                    speed_is_0 = True
                elif speed_is_0:
                    time_at_0 = end - start
                    if time_at_0 > 30:
                        data.append((start, time_at_0))
                    start = 0
                    end = 0
                    speed_is_0 = False
                else:
                    continue
        if start != 0:
            time_at_0 = end - start
            data.append((start, time_at_0))
        self.data = data

    def update_label(self):
        index = 0
        # Boucle sur les 15 valeur possibles
        for i in range(15):
            # Si on a des données à afficher, on affiche l'heure et le temps
            if i < len(self.data):
                current_data = self.data[i]
                hour = current_data[0]
                temps = current_data[1]
                # Mis à jour des textes
                self.labels_hours[i].setText(timestamp_to_hour_little(hour))
                self.labels_time[i].setText(str(timedelta(seconds=round(temps))))
                # Mis à jour des couleurs
                if temps <= 15 * 60:  # Moins de 15 minutes
                    self.labels_time[i].setStyleSheet("""
                        QLabel {
                            color: rgb(255, 255, 255);
                            font-size: 14px;
                            background-color: rgb(44, 62, 80)
                        }
                    """)
                elif temps <= 30 * 60:  # Entre 15 minutes et 30 minutes
                    self.labels_time[i].setStyleSheet("""
                        QLabel {
                            color: rgb(230, 126, 34);
                            font-size: 14px;
                            background-color: rgb(44, 62, 80)
                        }
                    """)
                else:  # Plus de 30 minutes
                    self.labels_time[i].setStyleSheet("""
                        QLabel {
                            color: rgb(230, 126, 34);
                            font-size: 14px;
                            background-color: rgb(44, 62, 80)
                        }
                    """)
            else:
                # Reset les labels avec un string vide
                self.labels_hours[i].setText("")
                self.labels_time[i].setText("")
                # Reset la couleur en blanc
                self.labels_time[i].setStyleSheet("""
                    QLabel {
                        color: rgb(255, 255, 255);
                        font-size: 14px;
                        background-color: rgb(44, 62, 80)
                    }
                """)

    def get_setting(self, prev_live, prev_day_ago, prev_zoom):
        self.day_ago = settings_store.day_ago
        self.get_data()
        self.update_label()
        self.update()

    def update_new_data(self):
        self.get_data()
        self.update_label()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        self.draw(p)
        p.end()

    def draw_fond(self, p):
        draw_rectangle(p, 0, 0, self.width(), self.height(), color_bleu_gris)

    def draw(self, p):
        self.draw_fond(p)
