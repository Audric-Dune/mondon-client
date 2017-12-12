# !/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import groupby


def affiche_entier(s, sep=' '):
    s = str(s)
    if len(s) <= 3:
        return s
    else:
        return affiche_entier(s[:-3]) + sep + s[-3:]


def clean_data_per_second(data, start, end):
    data_per_second = []  # Stock les valeurs nettoyées
    # Groupe les valeurs par secondes entières
    grouped = groupby(data, lambda v: int(v[0] / 1000))
    # Génère un dictionnaire avec pour clé la seconde et pour valeur la liste des vitesses
    # pour cette seconde
    values_per_second = {}
    for second, data_for_second in grouped:
        values_per_second[second] = [value[1] for value in data_for_second]
    # On boucle sur chaque seconde entre `start` et `end` (inclus) et calcule une vitesse pour
    # ces secondes.
    for i in range(int(start), int(end)):
        # Récupère les vitesses pour la seconde `i`.
        # Retourne un tableau vide si il n'y a pas de vitesses associées avec cette seconde
        ts = i
        values = values_per_second.get(ts, [])
        # Si on a trouvé des vitesses pour cette seconde, on prend la moyenne, sinon -0.001
        speed = sum(values) / len(values) if values else -0.001
        # Stocke dans clean_data
        data_per_second.append((ts, speed))
    data = _clean_data(data_per_second)
    return data


def _clean_data(data_per_second):
    data = []  # Stock les valeurs nettoyées
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
        data += data_for_speed
        previous_speed = speed
    return data
