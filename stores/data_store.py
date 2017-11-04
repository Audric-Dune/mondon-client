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
        self.start = start
        self.end = end
        self.day_ago = day_ago
        self.data = []
        self.dic_arret = {}
        self.arrets = []
        self.list_new_arret = []

    def add_data(self):
        try:
            new_data = Database.get_speeds(self.start * 1000, self.end * 1000)
            if not new_data:
                return False, []
            self.data = self.clean_data_per_second(new_data)
            self.data = self.clean_data(self.data)
            list_arrets_database = Database.get_arret(self.start, self.end)
            self.dic_arret_from_database(list_arrets_database)
            list_arrets_data = self.list_new_arret_data()
            self.update_dic_arret(list_arrets_data)
            self.arrets = self.convert_dic_to_array(self.dic_arret)
            print(self.list_new_arret)
            return True, self.list_new_arret
        except:
            return False, []

    @staticmethod
    def convert_dic_to_array(dic):
        """
        Convertie un dictionnaire (clé:start_arret, valeur:Arret) en un tableau de [start, end, type, raison]
        :param dic: Dictionnaire d'arrêt
        :return: Un tableau de data d'arret [start, end, type, raison]
        """
        # Initialisation du tableau à retourner
        array = []
        # Parcours les valeurs du dictionnaire
        for value in dic.items():
            # value[1] est l'object Arret du dictionnaire
            # Assigne les valeurs de l'arrêt dans tab
            start = value[1].start
            end = value[1].end
            type = value[1].type
            raison = value[1].raison
            tab = [start, end, type, raison]
            # Ajoute tab au tableau à retourner
            array.append(tab)
        return array

    def dic_arret_from_database(self, list_arrets_database):
        """
        S'occupe de créer les objects Arret et de les joindres au dictionnaire du store
        :param list_arrets_database: Tableau d'arret contenue en base de donnée pour le store
        """
        # On parcours le tableau d'arret contenue en base de donnée
        for arret_database in list_arrets_database:
            start_arret = arret_database[0]
            # Si l'arret et deja dans le dictionnaire on ne fait rien
            # La clé du dictionnaire est le début de l'arret
            if self.dic_arret.get(start_arret):
                continue
            # Sinon on ajoute un object Arret au dictionnaire avec les datas de la base de donnée
            else:
                from ui.widgets.arret import Arret
                object_arret = Arret(arret_database)
                self.dic_arret[start_arret] = object_arret

    def update_dic_arret(self, list_arrets_data):
        """
        S'occupe de créer un nouvelle arret en base de donnée si besoin
        Met a jour la fin d'un Arret contenue dans le dictionnaire si besoin
        :param list_arrets_data: Un tableau de tuple (start, end) définit par les vitesses de la base de donnée
        """
        self.list_new_arret = []
        # On parcours le tableau d'arret définit par les vitesses de la base de donnée
        for tuple_arret_data in list_arrets_data:
            start_arret = tuple_arret_data[0]
            end_arret = tuple_arret_data[1]
            # Si l'arret et deja dans le dictionnaire on test si la fin de l'arret est a jour
            # La clé du dictionnaire est le début de l'arret
            if self.dic_arret.get(start_arret):
                object_arret = self.dic_arret.get(start_arret)
                # Si la fin de l'arret n'est pas jour on l'update
                if object_arret.end != end_arret:
                    object_arret.end = end_arret
                    object_arret.update_arret()
            # Sinon on ajoute un object Arret au dictionnaire
            # On utilise les datas définit par les vitesses de la base de donnée
            else:
                from ui.widgets.arret import Arret
                arret_data = [start_arret, end_arret, "NULL", "NULL"]
                object_arret = Arret(arret_data)
                self.dic_arret[start_arret] = object_arret
                self.list_new_arret.append(start_arret)

    def list_new_arret_data(self):
        """
        S'occupe de créer la liste des arrêts machines du store par rapport aux nouvelles données
        :return: Un tableau de tuple de timestamp (début de l'arrêt, fin de l'arrêt)
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
                # Si on vient de sortir d'un arrêt on ajoute l'arrêt à la liste d'arrêts
                elif speed_is_0:
                    arrets.append((start, end))
                    start = 0
                    end = 0
                    speed_is_0 = False
                else:
                    continue
        # Si on sort de la boucle avec un arrêt en cours on ajoute le dernier arrêt à la liste d'arrêts
        if speed_is_0:
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
