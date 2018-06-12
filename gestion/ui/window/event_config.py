# !/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import Qt

from gestion.stores.settings_store import settings_store_gestion

from commun.constants.stylesheets import white_16_bold_label_stylesheet, \
    white_14_label_no_background_stylesheet, \
    button_little_stylesheet,\
    button_little_red_stylesheet,\
    white_text_edit_stylesheet,\
    red_12_label_stylesheet, green_12_label_stylesheet
from commun.ui.public.text_edit import TextEdit
from commun.ui.public.dropdown import Dropdown
from commun.utils.timestamp import timestamp_at_day_ago, timestamp_at_time, get_min_in_timestamp, get_hour_in_timestamp
from commun.constants.colors import color_bleu_gris


class EventConfig(QWidget):
    WIDTH_TEXT_EDIT = 30

    def __init__(self, type_event, event=None):
        super(EventConfig, self).__init__(None)
        self.setWindowFlags(Qt.Dialog)
        self.setFocusPolicy(Qt.ClickFocus)
        self.type_event = type_event
        if event:
            print(event)
        else:
            self.start = None
            self.duration = None
            self.end = None
            self.ensemble = None
            self.info = None
        self.status_label = QLabel()
        self.bt_valid = QPushButton("Validé")
        self.start_hour = TextEdit(number_only=True, number_min=6,
                                   number_max=22, width=self.WIDTH_TEXT_EDIT, alignement="center", init_value="")
        self.start_hour.textEdited.connect(lambda: self.on_settings_changed(value=self.start_hour.text(),
                                                                            name="start", unit="hour"))
        self.start_min = TextEdit(number_only=True, number_min=0, number_max=59,
                                  init_value=0, width=self.WIDTH_TEXT_EDIT, alignement="center", mode_min=True)
        self.start_min.textEdited.connect(lambda: self.on_settings_changed(value=self.start_min.text(),
                                                                           name="start", unit="min"))
        self.duration_hour = TextEdit(number_only=True, number_min=0,
                                      number_max=16, width=self.WIDTH_TEXT_EDIT, alignement="center", init_value="-")
        self.duration_hour.textEdited.connect(lambda: self.on_settings_changed(value=self.duration_hour.text(),
                                                                               name="duration", unit="hour"))
        self.duration_min = TextEdit(number_only=True, number_min=0, number_max=59,
                                     init_value="-", width=self.WIDTH_TEXT_EDIT, alignement="center", mode_min=True)
        self.duration_min.textEdited.connect(lambda: self.on_settings_changed(value=self.duration_min.text(),
                                                                              name="duration", unit="min"))
        self.end_hour = TextEdit(number_only=True, number_min=6,
                                 number_max=22, width=self.WIDTH_TEXT_EDIT, alignement="center", init_value="-")
        self.end_hour.textEdited.connect(lambda: self.on_settings_changed(value=self.end_hour.text(),
                                                                          name="end", unit="hour"))
        self.end_min = TextEdit(number_only=True, number_min=0, number_max=59,
                                init_value=0, width=self.WIDTH_TEXT_EDIT, alignement="center", mode_min=True)
        self.end_min.textEdited.connect(lambda: self.on_settings_changed(value=self.end_min.text(),
                                                                         name="end", unit="min"))
        self.init_widget()
        self.show()
        self.setFixedSize(self.size())
        self.update_bt_validate()

    def update_bt_validate(self):
        if self.is_valid_event():
            self.bt_valid.setDisabled(False)
        else:
            self.bt_valid.setDisabled(True)

    def is_valid_event(self):
        if self.start is None or self.end is None:
            self.status_label.setText("Début ou fin de l'événement non renseigné")
            self.status_label.setStyleSheet(red_12_label_stylesheet)
            return False
        if get_hour_in_timestamp(self.start) < 6:
            self.status_label.setText("Début de l'événement avant 06:00")
            self.status_label.setStyleSheet(red_12_label_stylesheet)
            return False
        if self.end < self.start:
            self.status_label.setText("Fin de l'événement supérieur au début")
            self.status_label.setStyleSheet(red_12_label_stylesheet)
            return False
        self.status_label.setText("Evénement valide")
        self.status_label.setStyleSheet(green_12_label_stylesheet)
        return True

    def on_settings_changed(self, value, name, unit):
        if name == "start":
            self.on_start_settings_changed(value=value, unit=unit)
        if name == "duration":
            self.on_duration_settings_changed(value=value, unit=unit)
        if name == "end":
            self.on_end_settings_changed(value=value, unit=unit)
        self.update_bt_validate()

    def on_start_settings_changed(self, value, unit):
        # Récupère les valeurs des champs start
        try:
            start_hour = int(self.start_hour.text())
        except ValueError:
            start_hour = None
        try:
            start_min = int(self.start_min.text())
        except ValueError:
            start_min = None
        if start_hour is None or start_min is None:
            self.start = None
        # Limite le start à 22h
        if unit == "min" and start_hour == 22:
            self.start_min.setText("00")
        if unit == "hour" and value == 22 and start_min > 0:
            self.start_min.setText("21")
        # Update le ts start
        if start_hour is not None and start_min is not None:
            self.start = self.get_timestamp_at_time(start_hour, start_min)
        # Calcul la durée et update les champs duration
        if self.start and self.end:
            self.duration = self.end - self.start
            self.update_text_edit(name="duration")
        # Calcul la fin et update les champs fin
        elif self.start and self.duration:
            self.end = self.start + self.duration
            self.update_text_edit(name="end")

    def on_duration_settings_changed(self, value, unit):
        # Récupère les valeurs des champs duration
        try:
            duration_hour = int(self.duration_hour.text())
        except ValueError:
            duration_hour = None
        # Update min à 00 si l'heure est renseigné et que la min est à "-"
        if duration_hour and self.duration_min.text() == "-":
            self.duration_min.setText("00")
        try:
            duration_min = int(self.duration_min.text())
        except ValueError:
            duration_min = None
        if duration_hour is None or duration_min is None:
            self.duration = None
        # Limite le duration à 22h
        if unit == "min" and duration_hour == 22:
            self.duration_min.setText("00")
        if unit == "hour" and value == 22 and duration_min > 0:
            self.duration_min.setText("21")
        # Update le ts duration
        if duration_hour is not None and duration_min is not None:
            self.duration = self.get_duration_time(hours=duration_hour, p_min=duration_min)
        # Calcul la fin et update les champs fin
        if self.start and self.duration:
            self.end = self.start + self.duration
            self.update_text_edit(name="end")
        # Calcul le start et update les champs start
        elif self.end and self.duration:
            self.start = self.end - self.duration
            self.update_text_edit(name="start")

    def on_end_settings_changed(self, value, unit):
        # Récupère les valeurs des champs end
        try:
            end_hour = int(self.end_hour.text())
        except ValueError:
            end_hour = None
        try:
            end_min = int(self.end_min.text())
        except ValueError:
            end_min = None
        if end_hour is None or end_min is None:
            self.end = None
        # Limite le end à 22h
        if unit == "min" and end_hour == 22:
            self.end_min.setText("00")
        if unit == "hour" and value == 22 and end_min > 0:
            self.end_min.setText("21")
        # Update le ts end
        if end_hour is not None and end_min is not None:
            self.end = self.get_timestamp_at_time(end_hour, end_min)
        # Calcul la durée et update les champs duration
        if self.start and self.end:
            self.duration = self.end - self.start
            self.update_text_edit(name="duration")
        # Calcul le start et update les champs start
        elif self.end and self.duration:
            self.start = self.end - self.duration
            self.update_text_edit(name="start")

    def update_text_edit(self, name):
        text_edit_hour = None
        text_edit_min = None
        ts = None
        if name == "start":
            text_edit_hour = self.start_hour
            text_edit_min = self.start_min
            ts = self.start
        if name == "duration":
            text_edit_hour = self.duration_hour
            text_edit_min = self.duration_min
        if name == "end":
            text_edit_hour = self.end_hour
            text_edit_min = self.end_min
            ts = self.end
        if text_edit_hour and text_edit_min and ts:
            if text_edit_hour.text() != str(get_hour_in_timestamp(ts)):
                text_edit_hour.setText(str(get_hour_in_timestamp(ts)))
            if text_edit_min.text() != str(get_min_in_timestamp(ts)):
                text_edit_min.setText(str(get_min_in_timestamp(ts)))
        else:
            if text_edit_hour.text() != str(self.get_hour_in_duration(self.duration)):
                text_edit_hour.setText(str(self.get_hour_in_duration(self.duration)))
            if text_edit_min.text() != str(self.get_min_in_duration(self.duration)):
                text_edit_min.setText(str(self.get_min_in_duration(self.duration)))

    @staticmethod
    def get_hour_in_duration(seconds):
        return int(seconds/3600)

    @staticmethod
    def get_min_in_duration(seconds):
        hours = int(seconds/3600)
        new_seconds = seconds - hours * 3600
        return int(new_seconds/60)

    @staticmethod
    def get_duration_time(hours, p_min):
        return (hours * 60 + p_min) * 60

    @staticmethod
    def get_timestamp_at_time(hours, p_min):
        ts_at_day_ago = timestamp_at_day_ago(settings_store_gestion.day_ago)
        ts = timestamp_at_time(ts=ts_at_day_ago, hours=hours, min=p_min)
        return ts

    def init_widget(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.addWidget(self.get_bloc_title())
        vbox.addWidget(self.get_bloc_settings())
        if self.type_event == "tool":
            vbox.addWidget(self.get_bloc_info())
        vbox.addWidget(self.get_bloc_bt())
        vbox.addWidget(self.status_label)
        self.setLayout(vbox)

    def get_bloc_title(self):
        title_contain = QWidget(parent=self)
        self.set_background_color(title_contain)
        title_label = QLabel(self.get_title())
        title_label.setStyleSheet(white_16_bold_label_stylesheet)
        title_contain_hbox = QHBoxLayout()
        title_contain_hbox.addWidget(title_label)
        title_contain.setLayout(title_contain_hbox)
        return title_contain

    def get_bloc_settings(self):
        settings_contain = QWidget(parent=self)
        self.set_background_color(settings_contain)
        settings_contain_vbox = QVBoxLayout()
        settings_contain_vbox.addLayout(self.get_line_setting("Début :", self.start_hour, self.start_min))
        settings_contain_vbox.addLayout(self.get_line_setting("Durée :", self.duration_hour, self.duration_min))
        settings_contain_vbox.addLayout(self.get_line_setting("Fin :", self.end_hour, self.end_min))
        settings_contain.setLayout(settings_contain_vbox)
        return settings_contain

    @staticmethod
    def get_line_setting(text, text_edit_hour, text_edit_min):
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        label = QLabel(text)
        label.setStyleSheet(white_14_label_no_background_stylesheet)
        hbox.addWidget(label)
        hbox.addStretch()
        hbox.addWidget(text_edit_hour)
        double_point_label = QLabel("h :")
        double_point_label.setStyleSheet(white_14_label_no_background_stylesheet)
        hbox.addWidget(double_point_label)
        hbox.addWidget(text_edit_min)
        min_label = QLabel("min")
        min_label.setStyleSheet(white_14_label_no_background_stylesheet)
        hbox.addWidget(min_label)
        return hbox

    def get_bloc_info(self):
        info_contain = QWidget(parent=self)
        self.set_background_color(info_contain)
        info_contain_vbox = QVBoxLayout()
        ensemble_dropdown = Dropdown(parent=self)
        ensemble_dropdown.set_placeholder("Sélectionner l'ensemble concerné")
        ensemble_dropdown_items = ["Colle à froid", "Enrouleurs", "Groupe appel enrouleur", "Calandre", "Colle à chaud",
                                   "Cadre guidage", "Groupe imprimeur", "Dérouleur papier", "Dérouleur polypro"]
        for item in ensemble_dropdown_items:
            ensemble_dropdown.add_item(item)
            ensemble_dropdown.VALUE_SELECTED_SIGNAL.connect(self.add_ensemble)
        info_contain_vbox.addWidget(ensemble_dropdown)
        info_text_edit = QTextEdit()
        info_text_edit.setPlaceholderText("Information complémentaire...")
        info_text_edit.setStyleSheet(white_text_edit_stylesheet)
        info_text_edit.setFixedHeight(50)
        info_text_edit.textChanged.connect(lambda: self.on_info_text_changed(info_text_edit))
        info_contain_vbox.addWidget(info_text_edit)
        info_contain.setLayout(info_contain_vbox)
        return info_contain

    def add_ensemble(self, text):
        self.ensemble = text

    def on_info_text_changed(self, text_edit):
        self.info = text_edit.toPlainText()

    def get_bloc_bt(self):
        bt_contain = QWidget(parent=self)
        self.set_background_color(bt_contain)
        bt_contain_hbox = QHBoxLayout()
        self.bt_valid.setStyleSheet(button_little_stylesheet)
        self.bt_valid.setFixedSize(80, 25)
        self.bt_valid.clicked.connect(self.save_event)
        bt_cancel = QPushButton("Annulé")
        bt_cancel.clicked.connect(self.close)
        bt_cancel.setStyleSheet(button_little_red_stylesheet)
        bt_cancel.setFixedSize(80, 25)
        bt_contain_hbox.addWidget(self.bt_valid)
        bt_contain_hbox.addWidget(bt_cancel)
        bt_contain.setLayout(bt_contain_hbox)
        return bt_contain

    def get_title(self):
        if self.type_event == "clean":
            return "Ajouter un nettoyage machine"
        if self.type_event == "stop":
            return "Ajouter un arrêt production"
        if self.type_event == "tool":
            return "Ajouter une action de maintenance"

    @staticmethod
    def set_background_color(widget):
        widget.setStyleSheet(
            "background-color:{color_bleu_gris};".format(color_bleu_gris=color_bleu_gris.hex_string)
        )

    def save_event(self):
        settings_store_gestion.save_event(self)
        self.close()
