# !/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import groupby
from time import time
from object.base_de_donnee import Database


current_time = time()


class DataStore:
    def __init__(self, start, end):
        self.data = []
        self.start = start
        self.end = end

    def add_data(self):
        new_data = Database.get_speeds(self.start * 1000, self.end * 1000)
        if not new_data:
            return False
        self.data = self.clean_data_per_second(new_data)
        self.data = self.clean_data(self.data)
        return True

    @staticmethod
    def clean_data_no(new_data):
        return [(value[0] / 1000, value[1]) for value in new_data]

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
        last_time = 0 # Stock la dernière valeur de vitesse
        count_no_value = 0 # Stock le nombre de fois qu'on a remplacé une valeur

        # Récupère le ts de la dernière valeur
        for data in data_per_second:
            if data[1] >= 0:
                last_time = data[0]

        clean_data = [] # Sotck les données clean
        previous_data = -0.001 # Stock la dernière valeur précédente de vitesse

        # On analyse chaque seconde du tableau de data par seconde
        for data in data_per_second:
            # Test d'arrêt lorsqu'on arrive à la dernière vitesse enregistrée
            if data[0] > last_time:
                break
            else:
                # Si on a une vitesse enregistrée on la met dans le tableau de data clean
                # Si on a pas de donnée depuis 5sec on considère que se n'est pas juste un lag de l'automate
                if data[1] >= 0 or count_no_value > 4:
                    clean_data.append((data[0], data[1]))
                    previous_data = data[1]
                    count_no_value = 0
                # Si on a pas de vitesse on considère que c'est un lag de l'autmate
                # et on remplace la valuer vide par la value précécente
                else:
                    clean_data.append((data[0], previous_data))
                    count_no_value += 1
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
