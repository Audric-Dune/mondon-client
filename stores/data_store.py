# !/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import groupby
from time import time

from ui.utils.timestamp import (
    timestamp_at_day_ago,
    timestamp_at_time,
    timestamp_to_day
)

from lib.base_de_donnee import Database


current_time = time()


class DataStore:
    def __init__(self, start, end, day_ago):
        self.day_ago = day_ago
        self.data = []
        self.arrets = []
        self.dechets = []
        self.start = start
        self.end = end

    def add_data(self):
        try:
            new_data = Database.get_speeds(self.start * 1000, self.end * 1000)
            if not new_data:
                return False
            self.data = self.clean_data_per_second(new_data)
            self.data = self.clean_data(self.data)
            arrets_data = self.list_new_arret()
            arrets_database = Database.get_arret(self.start * 1000, self.end * 1000)
            self.arrets = self.create_list_arret(arrets_data, arrets_database)
            print(self.arrets)
            return True
        except:
            return False

    @staticmethod
    def create_list_arret(arrets_data, arrets_database):
        """
        S'occupe de fusionner les arrêts déterminés avec les data et les arrêts contenus en base de donnée
        Si un arrêt_data n'est pas dans la base de donnée, il l'insert
        Si un arrêt_data n'est pas à jour, il l'update
        :param arrets_data: liste des arrêts déterminés avec les data
        :param arrets_database: liste des arrêts de la base de donnée
        :return: liste d'object "Arret" du store en cours
        """
        from ui.widgets.arret import Arret
        arrets = []
        # On parcours l'ensemble des arrêts déterminés avec les data
        for arret in arrets_data:
            arret_start = arret[0]
            arret_end = arret[1]
            # Pour chaque "arret_data" on parcour les arrêts de la base de donnée si il y en a
            if arrets_database:
                for arret_database in arrets_database:
                    # Si "arret_data" correspond à l'arrêt base donnée
                    # on regarde si la fin de l'arrêt à besoin d'être mis à jours
                    # Dans tous les cas on ajout un object "Arret" à la liste des arrêts
                    if arret_start == arret_database[0]:
                        arret_data = [arret_start, arret_end, arret_database[2], arret_database[3]]
                        arret = Arret(arret_data)
                        if arret_end != arret_database[1]:
                            arret.update()
                        arrets.append(arret)
                    # Sinon on ajoute l'arrêt en base de donnée et on ajoute l'object "Arret" à la liste des arrêts
                    else:
                        arret.create_on_database()
                    arrets.append(arret)
            # Si il n'y a pas d'arrêt en base de donnée on ajoute l'arrêt en base de donnée et on ajoute l'object
            # "Arret" à la liste des arrêts
            else:
                arret_data = [arret_start, arret_end, "NULL", "NULL"]
                arret_object = Arret(arret_data)
                arret_object.create_on_database()
                arrets.append(arret_object)
        return arrets

    def list_new_arret(self):
        """
        S'occupe de créer la liste des arrêts machines du store par rapport aux nouvelles données
        :return: Un tableau de tuple de timestamp (début de l'arrêt, durrée de l'arrêt)
        """
        # Récupère la liste des vitesses
        speeds = self.data
        # Récupère le timestamp du jours du store
        ts = timestamp_at_day_ago(self.day_ago)
        # Test si on est un vendredi
        vendredi = timestamp_to_day(ts) == "vendredi"
        # Les équipes commence toujours à 6H
        start = 6
        # La fin de journée est 22h sauf le vendredi 20h
        end = 20 if vendredi else 22
        # Définit les bornes de recherche d'arrêt dans les données
        start_ts = timestamp_at_time(ts, hours=start)
        end_ts = timestamp_at_time(ts, hours=end)
        # Initialisation des variables
        speed_is_0 = False
        arrets = []
        start = 0
        end = 0
        # On boucle sur le tableau de vitesse de store
        for value in speeds:
            # On test si la vitesse est dans la borne de recherche
            if value[0] < end_ts:
                # On test si la vitesse est inférieure à 60
                # On assimile une vitesse inférieure à 60 à machine à l'arrêt
                if 0 <= value[1] <= 60:
                    # Si on est pas déja dans un arrêt on définit le début de l'arrêt
                    if not speed_is_0:
                        start = value[0]
                    end = value[0]
                    speed_is_0 = True
                # Si on vient de sortir d'un arrêt et qu'il a durée plus de 10s, on ajoute l'arrêt à la liste d'arrêts
                elif speed_is_0:
                    time_at_0 = end - start
                    if time_at_0 > 10:
                        arrets.append((start, end))
                    start = 0
                    end = 0
                    speed_is_0 = False
                else:
                    continue
        # Si on sort de la boucle avec un arrêt en cours on ajoute le dernier arrêt à la liste d'arrêts
        if speed_is_0:
            time_at_0 = end - start
            if time_at_0 > 30:
                arrets.append((start, end))
        return arrets

    def clean_data_per_second(self, new_data):
        clean_data = []  # Stock les valeurs nettoyées

        # Groupe les valeurs par secondes entières
        grouped = groupby(new_data, lambda v: int(v[0] / 1000))

        # Génère un dictionnaire avec pour clé la seconde et pour valeur la liste des vitesses
        # pour cette seconde
        values_per_second = {}
        for second, data_for_second in grouped:
            values_per_second[second] = [value[1] for value in data_for_second]

        # On boucle sur chaque seconde entre `start` et `end` (inclus) et calcule une vitesse pour
        # ces secondes.
        for i in range(int(self.start), int(self.end) + 1):  # On inclus `end`
            # Récupère les vitesses pour la seconde `i`.
            # Retourne un tableau vide si il n'y a pas de vitesses associées avec cette seconde
            ts = i
            values = values_per_second.get(ts, [])
            # Si on a trouvé des vitesses pour cette seconde, on prend la moyenne, sinon -0.001
            speed = sum(values) / len(values) if values else -0.001
            # Stocke dans clean_data
            clean_data.append((ts, speed))

        return clean_data

    @staticmethod
    def clean_data(data_per_second):
        clean_data = []  # Stock les valeurs nettoyées

        # Groupe les valeurs par vitesse consécutive
        grouped = groupby(data_per_second, lambda v: v[1])

        previous_speed = -0.001
        for speed, data_for_speed in grouped:
            # Convertit l'itérateur en liste
            data_for_speed = list(data_for_speed)
            # Si la vitesse est une "abscence de vitesse" et si il y en a moins de 5 consécutive,
            # On remplace la vitesse par la vitesse précédente
            if speed == -0.001 and len(data_for_speed) < 10:
                data_for_speed = [(data[0], previous_speed) for data in data_for_speed]
            # Ajoute les valeurs au tableau de données clean
            clean_data += data_for_speed
            previous_speed = speed

        return clean_data

    def bisect(self, start_ts):
        size = len(self.data)
        low = 0
        high = size
        while low < high:
            mid = (low + high) // 2
            if start_ts < self.data[mid][0]:
                high = mid
            else:
                low = mid + 1
        return low

    def get_speed(self, start, end):
        result = []
        index = self.bisect(start)
        for i in range(index, len(self.data)):
            data = self.data[i]
            if start <= data[0] < end:
                result.append(data[1])
            elif data[0] >= end:
                break
        return sum(result) / len(result) if result else -1

    def get_last_speed(self):
        if self.data:
            for data in self.data:
                if data[1] >= 0:
                    last_data = data
            return last_data
        return None
