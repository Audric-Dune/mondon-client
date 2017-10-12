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
        return True

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
            # Si on a trouvé des vitesses pour cette seconde, on prend la moyenne, sinon -10
            speed = sum(values) / len(values) if values else -10
            # Stocke dans clean_data
            clean_data.append((ts, speed))

        return clean_data

    def clean_data(self, new_data):
        FENETRE_REPARTITION = 5
        clean_data = []
        # Initialisation de la fenêtre de travail
        start_fenetre = int(self.start)
        end_fenetre = int(start_fenetre + FENETRE_REPARTITION)
        data_fenetre = []
        fenetre_sans_valeur = [(ts * 1000, -0.00001) for ts in range(start_fenetre, end_fenetre)]

        # Parcours des données
        for data in new_data:
            ts = data[0]
            # Si la données est dans notre fenêtre de travaille courante
            # on la sauvegarde dans data_fenetre
            if start_fenetre * 1000 <= ts < end_fenetre * 1000:
                data_fenetre.append(data)
            # Sinon cela veut dire que l'on est plus dans la fenêtre
            else:
                # Processing de la fenêtre courante
                # 1. Si on a pas de valeur, on mets -10 sur toutes valeurs
                if len(data_fenetre) == 0:
                    data_fenetre = fenetre_sans_valeur
                # 2. Répartis les données temporellement
                # Cas particulier, si on a qu'une seul valeur, on la met au milieu de la fenêtre
                if len(data_fenetre) == 1:
                    data_fenetre = [(1000 * (start_fenetre + end_fenetre) / 2, data_fenetre[0][1])]
                # 3. Répartis les valeur de manière equidistante
                for i in range(len(data_fenetre)):
                    pos_dans_fenetre = i * FENETRE_REPARTITION / len(data_fenetre)
                    data_fenetre[i] = (1000 * (start_fenetre + pos_dans_fenetre), data_fenetre[i][1])
                # 4. Arrondis les timestamps à la seconde la plus proche
                clean_data_fenetre = []
                for data in data_fenetre:
                    clean_data_fenetre.append((int(data[0] / 1000), data[1]))
                data_fenetre = clean_data_fenetre
                # 5. Si on a pas assez de valeur, complete les valeurs
                if len(clean_data_fenetre) < FENETRE_REPARTITION:
                    # Traite le cas ou on a pas la premiere valeur:
                    # - On prend la moyenne entre la dernière valeur de la fenêtre précédente
                    #   et la prochaine valeur de la fenêtre
                    # - Si on est a pas de valeur dans la fenêtre prédédente, on utilise uniquement
                    #   la prochaine valeur de la fenêtre
                    if clean_data_fenetre[0][0] != start_fenetre:
                        next_speed = clean_data_fenetre[0][1]
                        prev_speed = next_speed
                        if len(data_fenetre) > 0:
                            prev_speed = data_fenetre[len(data_fenetre) - 1][1]
                        clean_data_fenetre.insert(0, (start_fenetre, (next_speed + prev_speed) / 2))
                    # Traite le cas ou on a pas la dernière valeur de la fenêtre:
                    # - On prend simplement la dernière valeur disponible de la fenêtre
                    last_value_fenetre = clean_data_fenetre[len(clean_data_fenetre) - 1]
                    if last_value_fenetre[0] != end_fenetre:
                        clean_data_fenetre.append((end_fenetre, last_value_fenetre[1]))
                    # Parcours toutes les secondes de la fenêtre et complète les valeurs manquantes
                    clean_clean_data_fenetre = []
                    for ts in range(start_fenetre, end_fenetre):
                        # Récupère la value dans clean_data_fenetre correspondant à `ts`
                        value = None
                        value_index = -1
                        for i in range(len(clean_data_fenetre)):
                            if clean_data_fenetre[i][0] == ts:
                                value = clean_data_fenetre[i]
                                value_index = i
                                break
                        # Si on en a pas (valeur manquante), on en crée une
                        if value is None:
                            prev_value = clean_data_fenetre[value_index - 1]
                            next_value = clean_data_fenetre[value_index + 1]
                            # La nouvelle valeur est une moyenne des deux valeurs les plus proches
                            # pondéré par leurs distance (en terme de timestamp)
                            distance_prev_value = abs(ts - prev_value[0])
                            distance_next_value = abs(next_value[0] - ts)
                            if distance_prev_value == 0:
                                new_value = prev_value
                            elif distance_next_value == 0:
                                new_value = next_value
                            else:
                                a = prev_value[1] * distance_next_value + next_value[1] * distance_prev_value
                                b = distance_next_value + distance_prev_value
                                new_value = a / b
                            clean_clean_data_fenetre.append((ts, new_value))
                        else:
                            clean_clean_data_fenetre.append(value)
                    clean_data_fenetre = clean_clean_data_fenetre
                # 6. Si on a trop de valeur, on remplace les groupes de valeur qui sont sur la
                #    même seconde, par une seule valeur qui est la moyenne du groupe
                if len(clean_data_fenetre) > FENETRE_REPARTITION:
                    clean_data_fenetre_dict = {}
                    new_clean_data_fenetre = []
                    for i in range(start_fenetre, end_fenetre):
                        clean_data_fenetre_dict[i] = []
                    for data in clean_data_fenetre:
                        clean_data_fenetre_dict[data[0]].append(data[1])
                    for second in range(start_fenetre, end_fenetre):
                        moyenne = sum(clean_data_fenetre_dict[second]) / len(clean_data_fenetre_dict[second])
                        new_clean_data_fenetre.append((second, moyenne))
                    clean_data_fenetre = new_clean_data_fenetre
                # 7. On ajoute les données propres à notre tableau global
                clean_data.append(clean_data_fenetre)

                # Initialisation de la fenêtre suivante
                start_fenetre += FENETRE_REPARTITION
                end_fenetre += FENETRE_REPARTITION
                data_fenetre = []

        clean_data = [item for sublist in clean_data for item in sublist]
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
