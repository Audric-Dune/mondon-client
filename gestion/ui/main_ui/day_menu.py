# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel

from commun.constants.colors import color_bleu_gris
from commun.constants.stylesheets import button_stylesheet, white_22_label_stylesheet, button_red_stylesheet
from commun.ui.public.mondon_widget import MondonWidget
from commun.ui.public.pixmap_button import PixmapButton
from commun.utils.timestamp import timestamp_at_day_ago, timestamp_to_date

from gestion.stores.settings_store import settings_store_gestion


class DayMenu(MondonWidget):
    PIXMAPBUTTON_SIZE = QSize(40, 40)
    BUTTON_HEIGHT = 40
    BUTTON_WIDTH = 100
    MINIMUN_WIDTH_LABEL = 350

    def __init__(self, parent):
        super(DayMenu, self).__init__(parent=parent)
        self.set_background_color(color_bleu_gris)
        self.master_hbox = QHBoxLayout()
        self.left_hbox = QHBoxLayout()
        self.center_hbox = QHBoxLayout()
        self.right_hbox = QHBoxLayout()
        self.bt_jour_plus = PixmapButton(parent=self)
        self.bt_jour_moins = PixmapButton(parent=self)
        self.bt_new_plan = PixmapButton(parent=self)
        self.bt_new_clean = PixmapButton(parent=self)
        self.bt_new_maintenance = PixmapButton(parent=self)
        self.bt_new_stop = PixmapButton(parent=self)
        self.bt_save_plan = PixmapButton(parent=self)
        self.bt_cancel_plan = PixmapButton(parent=self)
        self.bt_update_plan = PixmapButton(parent=self)
        self.bt_clear_plan = PixmapButton(parent=self)
        self.label_date = QLabel()
        self.init_widget()

    def init_widget(self):
        self.init_button()
        self.update_state_bt()
        self.setLayout(self.master_hbox)
        self.update_widget()

    def update_state_bt(self):
        if settings_store_gestion.plan_prod:
            if settings_store_gestion.plan_prod.is_valid():
                self.bt_save_plan.setEnabled(True)
            else:
                self.bt_save_plan.setEnabled(False)

    def update_widget(self):
        if settings_store_gestion.plan_prod:
            self.left_hbox.addWidget(self.bt_clear_plan)
            self.left_hbox.addWidget(self.bt_update_plan)
            self.bt_clear_plan.show()
            self.bt_update_plan.show()
        else:
            self.bt_clear_plan.hide()
            self.bt_update_plan.hide()
        self.left_hbox.addStretch(1)
        self.master_hbox.addLayout(self.left_hbox)

        if settings_store_gestion.plan_prod:
            self.bt_jour_moins.hide()
        else:
            self.center_hbox.addWidget(self.bt_jour_moins)
            self.center_hbox.addStretch(0)
            self.bt_jour_moins.show()

        self.center_hbox.addWidget(self.label_date)
        self.label_date.setStyleSheet(white_22_label_stylesheet)

        if settings_store_gestion.plan_prod:
            self.bt_jour_plus.hide()
        else:
            self.center_hbox.addStretch(0)
            self.center_hbox.addWidget(self.bt_jour_plus)
            self.bt_jour_plus.show()

        self.master_hbox.addLayout(self.center_hbox)

        self.right_hbox.addStretch(1)
        if settings_store_gestion.plan_prod:
            self.right_hbox.addWidget(self.bt_save_plan)
            self.right_hbox.addWidget(self.bt_cancel_plan)
            self.bt_save_plan.show()
            self.bt_cancel_plan.show()
            self.bt_new_clean.hide()
            self.bt_new_maintenance.hide()
            self.bt_new_stop.hide()
            self.bt_new_plan.hide()
        else:
            self.right_hbox.addWidget(self.bt_new_plan)
            self.right_hbox.addWidget(self.bt_new_clean)
            self.right_hbox.addWidget(self.bt_new_maintenance)
            self.right_hbox.addWidget(self.bt_new_stop)
            self.bt_save_plan.hide()
            self.bt_cancel_plan.hide()
            self.bt_new_plan.show()
            self.bt_new_clean.show()
            self.bt_new_maintenance.show()
            self.bt_new_stop.show()
        self.master_hbox.addLayout(self.right_hbox)
        self.update_label()

    def init_button(self):
        # Bouton jour plus
        self.bt_jour_plus.setToolTip("Changement jours")
        self.bt_jour_plus.clicked.connect(self.jour_plus)
        self.bt_jour_plus.setStyleSheet(button_stylesheet)
        self.bt_jour_plus.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_jour_plus.addImage("commun/assets/images/fleche_suivant.png")

        # Bouton jour moins
        self.bt_jour_moins.setToolTip("Changement jours")
        self.bt_jour_moins.clicked.connect(self.jour_moins)
        self.bt_jour_moins.setStyleSheet(button_stylesheet)
        self.bt_jour_moins.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_jour_moins.addImage("commun/assets/images/fleche_precedent.png")

        # Bouton nouveau plan
        self.bt_new_plan.setToolTip("Ajouter un nouveau plan de production")
        self.bt_new_plan.clicked.connect(self.create_new_plan)
        self.bt_new_plan.setStyleSheet(button_stylesheet)
        self.bt_new_plan.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_new_plan.addImage("commun/assets/images/icon_add_prod.png")

        # Bouton nouveau nettoyage
        self.bt_new_clean.setToolTip("Ajouter une nouvelle période de nettoyage")
        self.bt_new_clean.clicked.connect(lambda: self.create_new_event(type_event="clean"))
        self.bt_new_clean.setStyleSheet(button_stylesheet)
        self.bt_new_clean.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_new_clean.addImage("commun/assets/images/icon_add_clean_prod.png")

        # Bouton nouvelle maintenance
        self.bt_new_maintenance.setToolTip("Ajouter une nouvelle action de maintenance")
        self.bt_new_maintenance.setStyleSheet(button_stylesheet)
        self.bt_new_maintenance.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_new_maintenance.addImage("commun/assets/images/icon_add_maintenance_prod.png")

        # Bouton nouvelle période sans production
        self.bt_new_stop.setToolTip("Ajouter une nouvelle période sans production")
        self.bt_new_stop.setStyleSheet(button_stylesheet)
        self.bt_new_stop.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_new_stop.addImage("commun/assets/images/icon_add_stop_prod.png")

        # Bouton sauvegarde plan
        self.bt_save_plan.setToolTip("Enregistrer le plan de production")
        self.bt_save_plan.clicked.connect(self.save_plan_prod)
        self.bt_save_plan.setStyleSheet(button_stylesheet)
        self.bt_save_plan.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_save_plan.addImage("commun/assets/images/save_as.png")

        # Bouton annuler plan
        self.bt_cancel_plan.setToolTip("Annuler l'ajout du plan de production")
        self.bt_cancel_plan.clicked.connect(self.cancel_plan)
        self.bt_cancel_plan.setStyleSheet(button_red_stylesheet)
        self.bt_cancel_plan.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_cancel_plan.addImage("commun/assets/images/white_cross.png")

        # Bouton mettre à jours plan
        self.bt_update_plan.setToolTip("Mettre à jours le plan de production")
        self.bt_update_plan.clicked.connect(self.update_plan)
        self.bt_update_plan.setStyleSheet(button_stylesheet)
        self.bt_update_plan.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_update_plan.addImage("commun/assets/images/icon_update.png")

        # Bouton effacer plan
        self.bt_clear_plan.setToolTip("Réinitialiser le plan de production")
        self.bt_clear_plan.clicked.connect(self.clear_plan)
        self.bt_clear_plan.setStyleSheet(button_stylesheet)
        self.bt_clear_plan.setFixedSize(self.PIXMAPBUTTON_SIZE)
        self.bt_clear_plan.addImage("commun/assets/images/clear.png")

    def on_settings_gestion_changed(self):
        self.update_widget()

    def update_label(self):
        ts = timestamp_at_day_ago(settings_store_gestion.day_ago)
        date = timestamp_to_date(ts).capitalize()
        self.label_date.setMinimumWidth(self.MINIMUN_WIDTH_LABEL)
        self.label_date.setAlignment(Qt.AlignCenter)
        self.label_date.setText(date)

    @staticmethod
    def jour_moins():
        settings_store_gestion.set_day_ago(settings_store_gestion.day_ago + 1)

    @staticmethod
    def jour_plus():
        settings_store_gestion.set_day_ago(settings_store_gestion.day_ago - 1)

    @staticmethod
    def create_new_plan():
        settings_store_gestion.create_new_plan()

    @staticmethod
    def create_new_event(type_event):
        settings_store_gestion.create_new_event(type_event)

    @staticmethod
    def save_plan_prod():
        if settings_store_gestion.plan_prod.is_valid():
            settings_store_gestion.save_plan_prod()
            from gestion.stores.plan_prod_store import plan_prod_store
            plan_prod_store.get_plan_prod_from_database()

    @staticmethod
    def clear_plan():
        settings_store_gestion.plan_prod.clear_plan_prod()

    @staticmethod
    def cancel_plan():
        settings_store_gestion.cancel_plan_prod()

    @staticmethod
    def update_plan():
        settings_store_gestion.plan_prod.get_new_item_selected_from_store()
