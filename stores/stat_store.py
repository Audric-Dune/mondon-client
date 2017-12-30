# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject
from statistics import mean
from lib.base_de_donnee import Database
from constants.param import VITESSE_MOYENNE_MAXI, DEBUT_PROD_MATIN, FIN_PROD_SOIR, FIN_PROD_SOIR_VENDREDI
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
    data_type = settings_stat_store.data_type
    week_ago = settings_stat_store.week_ago
    month_ago = settings_stat_store.month_ago
    year_ago = settings_stat_store.year_ago

    def __init__(self):
        super(StatStore, self).__init__()
        self.data_on_database = []
        self.data = None
        self.stat = None

    def init_var(self):
        """
        Initialise les variables data et stat en fonction du type de data sélectionner dans settings stat store
        """
        if self.data_type == "metrage":
            self.data = {"matin": [], "soir": [], "total": []}
            self.stat = {"matin": {}, "soir": {}, "total": {}}

    def update_data(self):
        if self.get_data():
            self.ON_DATA_STAT_CHANGED_SIGNAL.emit()
            print(self.data)
            print(self.stat)

    def get_data(self):
        """
        Génère les données en fonction des settings du settings_stat_store
        :return: True si il y a de nouvelle data
        """
        data_time = self.get_start_end()
        start = data_time[0]
        end = data_time[1]
        new_data_on_database = self.get_data_on_database(start, end)
        if self.data_on_database == new_data_on_database:
            return False
        else:
            self.data_on_database = new_data_on_database
        self.init_var()
        if self.data_on_database:
            # GESTION DES DATA METRAGE PAR JOUR
            if self.data_type == "metrage" and self.year_ago < 0:
                # On parcour tout les jours entre start et end
                current_day = start
                while current_day < end:
                    data = []
                    # Vérifie si on est pas dans un jours du weekend
                    if not self.is_weekend(ts_day=current_day):
                        # Récupère les data du ts courant dans les data en database
                        data = self.get_data_on_ts(data=self.data_on_database, ts=current_day)
                        # Si elle n'y sont pas cherche dans les stores existants
                        if not data:
                            data_store = data_store_manager.get_store_at_time(current_day)
                            # Si elle n'y sont pas crée un nouveau store
                            if not data_store:
                                data_store = data_store_manager.add_new_store(current_day)
                            data.append(round(current_day))
                            data.append(data_store.metrage_matin)
                            data.append(data_store.metrage_soir)
                    # Ajoute les data du jour courant au data générale
                    self.add_data_metrage(data)
                    # Passe au jour suivant
                    current_day = timestamp_after_day_ago(start=current_day, day_ago=1)
        self.get_stat()
        return True

    def get_stat(self):
        """
        Génère les statistiques issues des données récupérées dans get_data
        """
        data_time = self.get_start_end()
        start = data_time[0]
        end = data_time[1]
        if self.data:
            total_time_prod = self.get_total_time_prod(start, end)
            if self.data_type == "metrage":
                self.stat["matin"] = self.stat_calculator(moment="matin", total_time_prod=total_time_prod)
                self.stat["soir"] = self.stat_calculator(moment="soir", total_time_prod=total_time_prod)
                self.stat["total"] = self.stat_calculator(moment="total", total_time_prod=total_time_prod)

    def get_start_end(self):
        """
        Récupère les valeurs de début et fin des data en fonction des settings
        :return: Un tuple (début, fin)
        """
        start_ts = 0
        end_ts = 0
        if self.week_ago >= 0:
            start_ts = timestamp_at_week_ago(self.week_ago)
            if self.week_ago == 0:
                end_ts = timestamp_now()
            else:
                end_ts = timestamp_at_week_ago(self.week_ago - 1)
        if self.month_ago >= 0:
            start_ts = timestamp_at_month_ago(self.month_ago)
            if self.month_ago == 0:
                end_ts = timestamp_now()
            else:
                end_ts = timestamp_at_month_ago(self.month_ago - 1)
        return start_ts, end_ts

    def get_data_on_database(self, start, end):
        """
        Récupère les données en base de donnée
        :param start: Début des données a récupérer
        :param end: Fin des données a récupérer
        :return: Les données
        """
        data = []
        if self.data_type == "metrage":
            data = Database.get_metrages(start_time=start, end_time=end)
            data.sort()
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
        Ajoute une série de data au data globals
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

    def get_total_time_prod(self, start, end):
        """
        Calcul le temps de production entre deux ts
        :param start: Ts de début du calcul
        :param end:  Ts de fin du calcul
        :return: Le temps de production en s
        """
        total_time_prod = 0
        if self.data_type == "metrage":
            # On parcour tout les jours entre start et end
            current_day = start
            while current_day < end:
                # Vérifie si on est pas dans un jours du weekend
                if not self.is_weekend(ts_day=current_day):
                    # On calcul le temps de production d'un journée normal
                    current_time_prod = (FIN_PROD_SOIR - DEBUT_PROD_MATIN) * 3600
                    # On modifie le temps de production si on est vendredi
                    vendredi = self.is_vendredi(ts_day=current_day)
                    if vendredi:
                        current_time_prod = (FIN_PROD_SOIR_VENDREDI - DEBUT_PROD_MATIN) * 3600
                    # On modifie le temps de production si on est en cour de journée
                    if self.day_not_finish(ts_day=current_day, vendredi=vendredi):
                        current_time_prod = end - timestamp_at_time(end, hours=DEBUT_PROD_MATIN)
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
    def day_not_finish(ts_day, vendredi):
        """
        Regarde si le jour est en cour
        :param ts_day: le timestamp du jour
        :param vendredi: True si on est vendredi sinon False
        :return: True si le jour est en cour sinon False
        """
        fin_prod = FIN_PROD_SOIR_VENDREDI if vendredi else FIN_PROD_SOIR
        return timestamp_now() < timestamp_at_time(ts_day, hours=fin_prod)

    def stat_calculator(self, moment, total_time_prod):
        """
        Calcul les statistiques de la série "moment"
        :param moment: Le moment étudié (matin, soir, ou total)
        :param total_time_prod: Temps de production total de la série total
        :return: Un dictionnaire contenant les statistiques : total, max, mean, percent
        """
        dic_stat = {}
        values = [t[1] for t in self.data[moment]]
        sum_data = sum(values)
        max_data = max(values)
        mean_data = mean(values)
        total_time_prod = total_time_prod if moment == "total" else total_time_prod / 2
        max_prod = total_time_prod * VITESSE_MOYENNE_MAXI
        percent_prod = 0
        if max_prod:
            percent_prod = sum_data * 100 / max_prod
        dic_stat["total"] = sum_data
        dic_stat["max"] = max_data
        dic_stat["percent"] = round(percent_prod, 2)
        dic_stat["mean"] = round(mean_data)
        return dic_stat


stat_store = StatStore()
