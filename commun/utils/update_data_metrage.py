# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.utils.data import clean_data_per_second

from commun.constants.param import (
    DEBUT_PROD_MATIN,
    FIN_PROD_MATIN,
    FIN_PROD_MATIN_VENDREDI,
    FIN_PROD_SOIR, )
from commun.lib.base_de_donnee import Database
from commun.utils.timestamp import timestamp_at_day_ago, timestamp_at_time, timestamp_to_day, timestamp_after_day_ago


def update_data_metrage():
    """
    Donnee enregistree de maniere fiable depuis le 23/10/2017 semaine 43 (timestamp: 1508709600)
    Fonction appele a chaque demarrage de l'application
    Parcour tout les jours depuis le 23/10/2017 jusqu'a hier
    Verifie si les donnees metrages de chaque jour est renseigne en base de donnee
    Si les donnees metrages n'existes pas on les calculs et on les inserts en base de donnee
    """
    def get_jour_metrage():
        """
        Recupere les jours ou les metrages sont deja renseignees en base de donnee
        :return: Une liste des jours
        """
        list_jour_metrage = Database.get_all_jour_metrages()
        clean_list = []
        for jour_metrage in list_jour_metrage:
            ts = jour_metrage[0]
            clean_list.append(ts)
        return clean_list

    def is_vendredi(ts):
        """
        Test si le jour d'un timestamp est vendredi
        :param ts: L etimestamp a tester
        :return: True si on est vendredi
        """
        return timestamp_to_day(ts) == "vendredi"

    def get_metrage(data, vendredi):
        """
        Calcul les metrages de l'equipe du matin et du soir
        Prend en compte si on est vendredi
        :param data: Les donnees triees par seconde
        :param vendredi: True si on traite des donnees d'un vendredi
        :return: Les valeurs arrondies du metrage matin et soir
        """
        metrage_matin = 0
        metrage_soir = 0
        fin_prod_matin = FIN_PROD_MATIN_VENDREDI if vendredi else FIN_PROD_MATIN
        for value in data:
            ts = value[0]
            metrage = value[1] / 60 if value[1] > 0 else 0
            if ts < timestamp_at_time(ts, hours=fin_prod_matin):
                metrage_matin += metrage
            else:
                metrage_soir += metrage
        return round(metrage_matin), round(metrage_soir)

    # On recupere la liste des jours ou le metrage est renseigne en base de donnee
    list_jour_metrage_on_db = get_jour_metrage()
    # Debut des donnees fiable
    start_data_record = 1508709600
    # Duree d'un jour en ms
    ts_to_one_day = 86400
    # Timestamp du debut du jour actuel
    start_ts_of_current_day = timestamp_at_day_ago(day_ago=0)
    start_day = start_data_record
    while start_day < start_ts_of_current_day:
        if start_day in list_jour_metrage_on_db:
            pass
        else:
            start_time = timestamp_at_time(ts=start_day, hours=DEBUT_PROD_MATIN)
            end_time = timestamp_at_time(start_day, hours=FIN_PROD_SOIR)
            speed_data = Database.get_speeds(start_time=start_time*1000, end_time=end_time*1000)
            clean_speed_data = clean_data_per_second(speed_data, start_time, end_time)
            total_metrage = get_metrage(data=clean_speed_data, vendredi=is_vendredi(start_day))
            Database.insert_jour_metrages(ts_jour=start_day,
                                          metrage_matin=total_metrage[0],
                                          metrage_soir=total_metrage[1])
        start_day = timestamp_after_day_ago(start_day, day_ago=1)
    return True
