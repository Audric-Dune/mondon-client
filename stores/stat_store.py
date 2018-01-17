# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject
from statistics import mean
from lib.base_de_donnee import Database
from constants.param import VITESSE_MOYENNE_MAXI,\
    DEBUT_PROD_MATIN,\
    FIN_PROD_SOIR,\
    FIN_PROD_SOIR_VENDREDI,\
    FIN_PROD_MATIN,\
    FIN_PROD_MATIN_VENDREDI
from stores.data_store_manager import data_store_manager

from ui.utils.timestamp import timestamp_at_week_ago,\
    timestamp_now,\
    timestamp_at_month_ago,\
    timestamp_after_day_ago,\
    timestamp_to_day,\
    timestamp_at_time
from stores.settings_stat_store import settings_stat_store


class StatStore(QObject):
    ON_DATA_STAT_CHANGED_SIGNAL = pyqtSignal()

    def __init__(self):
        super(StatStore, self).__init__()
        self.data_on_database = []
        self.data = None
        self.stat = None

    def init_var(self):
        """
        Initialise les variables data et stat en fonction du type de data sélectionner dans settings stat store
        """
        if settings_stat_store.data_type == "métrage":
            self.data = {"matin": [], "soir": [], "total": []}
            self.stat = {"matin": {}, "soir": {}, "total": {}}
        if settings_stat_store.data_type == "temps":
            self.data = {"Prévu": [], "Imprévu": [], "total": []}
            self.stat = {"Prévu": {}, "Imprévu": {}, "total": {}}
        if settings_stat_store.data_type == "raisons_prévue":
            self.data = {}
            self.stat = {}
        if settings_stat_store.data_type == "raisons_imprévue":
            self.data = {}
            self.stat = {}

    def update_data(self):
        if self.get_data():
            self.ON_DATA_STAT_CHANGED_SIGNAL.emit()

    @staticmethod
    def get_data_store(ts_day):
        data_store = data_store_manager.get_store_at_time(ts_day)
        # Si elle n'y sont pas crée un nouveau store
        if not data_store:
            data_store = data_store_manager.add_new_store(ts_day)
        return data_store

    def get_data(self):
        """
        Génère les données en fonction des settings du settings_stat_store
        :return: True si il y a de nouvelle data
        """
        data_time = self.get_start_end()
        start = data_time[0]
        end = data_time[1]
        self.data_on_database = self.get_data_on_database(start, end)
        self.init_var()
        if self.data_on_database:
            if settings_stat_store.data_type == "métrage" or settings_stat_store.data_type == "temps":
                self.get_data_metrage_or_temps(start, end)
            else:
                self.get_data_raisons()
        self.get_stat()
        return True

    def get_data_metrage_or_temps(self, start, end):
        if settings_stat_store.year_ago < 0:
            # On parcour tout les jours entre start et end
            current_day = start
            while current_day < end:
                data = []
                # Vérifie si on est pas dans un jours du weekend
                if not self.is_weekend(ts_day=current_day):
                    if settings_stat_store.data_type == "métrage":
                        # Récupère les data du ts courant dans les data en database
                        data = self.get_data_on_ts(data=self.data_on_database, ts=current_day)
                        if not data:
                            data_store = self.get_data_store(ts_day=current_day)
                            data.append(round(current_day))
                            data.append(data_store.metrage_matin)
                            data.append(data_store.metrage_soir)
                    elif settings_stat_store.data_type == "temps":
                        data_store = self.get_data_store(ts_day=current_day)
                        data.append(round(current_day))
                        data.append(data_store.arret_time_matin + data_store.arret_time_soir)
                        data.append(data_store.imprevu_arret_time_matin + data_store.imprevu_arret_time_soir)
                # Ajoute les data du jour courant au data générale
                if settings_stat_store.data_type == "métrage":
                    self.add_data_metrage(data)
                elif settings_stat_store.data_type == "temps":
                    self.add_data_temps(data)
                # Passe au jour suivant
                current_day = timestamp_after_day_ago(start=current_day, day_ago=1)

    def get_data_raisons(self):
        list_arret = self.data_on_database[0]
        list_raisons = self.data_on_database[1]
        self.data = {}
        for arret in list_arret:
            arret_start = arret[0]
            arret_end = arret[1]
            raison = self.get_raison(list_raisons, arret_start)
            if raison:
                raison_type = raison[2]
                raison_texte = raison[3]
                if raison_texte[0:5] == "Autre":
                    raison_texte = "Autre"
                if raison_type == "Prévu" if settings_stat_store.data_type == "raison prévue" else "Imprévu":
                    if self.data.get(raison_texte):
                        count = self.data[raison_texte][0] + 1
                        total_time = self.data[raison_texte][1] + (arret_end - arret_start)
                    else:
                        count = 1
                        total_time = arret_end - arret_start
                    self.data[raison_texte] = [count, total_time]
                print(self.data)
            else:
                continue

    @staticmethod
    def get_raison(raisons, start):
        for raison in raisons:
            if raison[1] == start and raison[4] == 1:
                return raison

    def get_stat(self):
        """
        Génère les statistiques issues des données récupérées dans get_data
        """
        if self.data:
            if settings_stat_store.data_type == "métrage":
                self.stat["matin"] = self.stat_calculator_metrage(moment="matin")
                self.stat["soir"] = self.stat_calculator_metrage(moment="soir")
                self.stat["total"] = self.stat_calculator_metrage(moment="total")
            if settings_stat_store.data_type == "temps":
                self.stat["Prévu"] = self.stat_calculator_temps(type="Prévu")
                self.stat["Imprévu"] = self.stat_calculator_temps(type="Imprévu")
                self.stat["total"] = self.stat_calculator_temps(type="total")

    @staticmethod
    def get_start_end():
        """
        Récupère les valeurs de début et fin des data en fonction des settings
        :return: Un tuple (début, fin)
        """
        start_ts = 0
        end_ts = 0
        if settings_stat_store.week_ago >= 0:
            start_ts = timestamp_at_week_ago(settings_stat_store.week_ago)
            if settings_stat_store.week_ago == 0:
                end_ts = timestamp_now()
            else:
                end_ts = timestamp_at_week_ago(settings_stat_store.week_ago - 1)
        if settings_stat_store.month_ago >= 0:
            start_ts = timestamp_at_month_ago(settings_stat_store.month_ago)
            if settings_stat_store.month_ago == 0:
                end_ts = timestamp_now()
            else:
                end_ts = timestamp_at_month_ago(settings_stat_store.month_ago - 1)
        return start_ts, end_ts

    @staticmethod
    def get_data_on_database(start, end):
        """
        Récupère les données en base de donnée
        :param start: Début des données a récupérer
        :param end: Fin des données a récupérer
        :return: Les données
        """
        data = []
        if settings_stat_store.data_type == "métrage":
            data = Database.get_metrages(start_time=start, end_time=end)
            data.sort()
        elif settings_stat_store.data_type == "temps":
            data = Database.get_arret(start_time=start, end_time=end)
        else:
            data = [Database.get_arret(start_time=start, end_time=end),
                    Database.get_raison(start_time=start, end_time=end)]
        return data

    @staticmethod
    def is_weekend(ts_day):
        """
        Test si un ts correspond à un jour du weekend (samedi ou dimanche)
        :return: True si le ts correspond a un samedi ou dimanche sinon False
        """
        day = timestamp_to_day(ts_day)
        return day == "samedi" or day == "dimanche"

    @staticmethod
    def get_data_on_ts(data, ts):
        """
        S'occupe de retrouver une série de donnée correspondant à un ts
        :param data: Les données à parcourir
        :param ts: Le timestamp recherché
        :return: La série de valeurs trouvé ou False
        """
        for values in data:
            ts_value = values[0]
            if ts_value == ts:
                return values
        return []

    def add_data_metrage(self, data):
        """
        Ajoute une série de data métrage au data globals
        :param data: Les data à ajouter
        """
        if data:
            ts = data[0]
            metrage_matin = data[1]
            metrage_soir = data[2]
            metrage_total = metrage_matin + metrage_soir
            self.data["matin"].append((ts, metrage_matin))
            self.data["soir"].append((ts, metrage_soir))
            self.data["total"].append((ts, metrage_total))

    def add_data_temps(self, data):
        """
        Ajoute une série de data temps au data globals
        :param data: Les data à ajouter
        """
        if data:
            ts = data[0]
            metrage_total = data[1]
            metrage_imprevu = data[2]
            metrage_prevu = metrage_total - metrage_imprevu
            self.data["Prévu"].append((ts, metrage_prevu))
            self.data["Imprévu"].append((ts, metrage_imprevu))
            self.data["total"].append((ts, metrage_total))

    def get_total_time_prod(self, moment):
        """
        Calcul le temps de production entre deux ts
        :param moment: Permet d'identifier la plage d'étude (matin, soir, total)
        :return: Le temps de production en s
        """
        data_time = self.get_start_end()
        start = data_time[0]
        end = data_time[1]
        total_time_prod = 0
        # On parcour tout les jours entre start et end
        current_day = start
        while current_day < end:
            # Vérifie si on est pas dans un jours du weekend
            if not self.is_weekend(ts_day=current_day):
                # On calcul le temps de production d'une journée normal
                current_time_prod = (FIN_PROD_SOIR - DEBUT_PROD_MATIN) * 3600
                # On modifie le temps de production si on est vendredi
                vendredi = self.is_vendredi(ts_day=current_day)
                if vendredi:
                    current_time_prod = (FIN_PROD_SOIR_VENDREDI - DEBUT_PROD_MATIN) * 3600
                # Si la période est une demi-journée on divise par 2
                if moment == "matin" or moment == "soir":
                    current_time_prod /= 2
                # On modifie le temps de production si on est en cour de journée
                if self.day_not_finish(ts_day=current_day, vendredi=vendredi, moment=moment):
                    if moment == "soir":
                        debut_prod = FIN_PROD_MATIN_VENDREDI if vendredi else FIN_PROD_MATIN
                    else:
                        debut_prod = DEBUT_PROD_MATIN
                    if timestamp_now() - timestamp_at_time(end, hours=debut_prod) < 0:
                        break
                    current_time_prod = timestamp_now() - timestamp_at_time(end, hours=debut_prod)
                total_time_prod += current_time_prod
            # Passe au jour suivant
            current_day = timestamp_after_day_ago(start=current_day, day_ago=1)
        return total_time_prod

    @staticmethod
    def is_vendredi(ts_day):
        """
        Test si un ts correspond à un vendredi
        :return: True si le ts correspond a un vendredi sinon False
        """
        day = timestamp_to_day(ts_day)
        return day == "vendredi"

    @staticmethod
    def day_not_finish(ts_day, vendredi, moment):
        """
        Regarde si le jour est en cour
        :param ts_day: le timestamp du jour
        :param vendredi: True si on est vendredi sinon False
        :param moment: Période étudiée
        :return: True si le jour est en cour sinon False
        """
        if moment == "matin":
            fin_prod = FIN_PROD_MATIN_VENDREDI if vendredi else FIN_PROD_MATIN
        else:
            fin_prod = FIN_PROD_SOIR_VENDREDI if vendredi else FIN_PROD_SOIR
        return timestamp_now() < timestamp_at_time(ts_day, hours=fin_prod)

    @staticmethod
    def empty_stat():
        return {
            'total': 0,
            'max': 0,
            'percent': 0,
            'mean': 0,
        }

    def stat_calculator_metrage(self, moment):
        """
        Calcul les statistiques de la série "moment"
        :param moment: Le moment étudié (matin, soir, ou total)
        :return: Un dictionnaire contenant les statistiques : total, max, mean, percent
        """
        data = self.data[moment]
        if not data:
            return self.empty_stat()
        dic_stat = {}
        values = [t[1] for t in data]
        sum_data = sum(values)
        max_data = max(values)
        mean_data = mean(values)
        total_time_prod = self.get_total_time_prod(moment)
        max_prod = total_time_prod * VITESSE_MOYENNE_MAXI / 60
        percent_prod = 0
        if max_prod:
            percent_prod = sum_data * 100 / max_prod
        dic_stat["total"] = sum_data
        dic_stat["max"] = max_data
        dic_stat["percent"] = round(percent_prod, 2)
        dic_stat["mean"] = round(mean_data)
        return dic_stat

    def stat_calculator_temps(self, type):
        data = self.data[type]
        if not data:
            return self.empty_stat()
        dic_stat = {}
        values = [t[1] for t in data]
        sum_data = sum(values)
        max_data = max(values)
        mean_data = mean(values)
        total_time_prod = self.get_total_time_prod("total")
        percent_prod = 0
        if total_time_prod:
            percent_prod = sum_data * 100 / total_time_prod
        dic_stat["total"] = sum_data
        dic_stat["max"] = max_data
        dic_stat["percent"] = round(percent_prod, 2)
        dic_stat["mean"] = round(mean_data)
        return dic_stat

stat_store = StatStore()
