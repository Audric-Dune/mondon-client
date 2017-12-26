# !/usr/bin/env python
# -*- coding: utf-8 -*-
from constants.param import DEBUT_PROD_MATIN, FIN_PROD_MATIN_VENDREDI, FIN_PROD_MATIN, FIN_PROD_SOIR, FIN_PROD_SOIR_VENDREDI, VITESSE_LIMITE_ASSIMILATION_ARRET

from lib.base_de_donnee import Database
from ui.utils.data import clean_data_per_second
from ui.utils.timestamp import (timestamp_at_day_ago, timestamp_at_time, timestamp_to_day)


class DataStore:
    def __init__(self, start, end, day_ago):
        self.start = start
        self.end = end
        self.day_ago = day_ago
        self.data = []
        self.metrage_matin = 0
        self.metrage_soir = 0
        self.arret_time_matin = 0
        self.imprevu_arret_time_matin = 0
        self.arret_time_soir = 0
        self.imprevu_arret_time_soir = 0
        self.dic_arret = {}
        self.arrets = []

    def add_data(self):
        try:
            new_data = Database.get_speeds(self.start * 1000, self.end * 1000)
            if not new_data:
                return False, []
            self.data = clean_data_per_second(data=new_data, start=self.start, end=self.end)
            ts = timestamp_at_day_ago(self.day_ago)
            if self.day_ago > 0:
                metrage = Database.get_metrages_for_one_day(start_time=ts)
                metrage = metrage[0]
                if not metrage:
                    metrage = self.get_live_stat(self.data, ts)
            else:
                metrage = self.get_live_stat(self.data, ts)
            self.metrage_matin = metrage[0]
            self.metrage_soir = metrage[1]

            list_arrets_database = Database.get_arret(self.start, self.end)
            self.dic_arret_from_database(list_arrets_database)
            list_arrets_data = self.list_new_arret_data()
            list_new_arret = self.update_dic_arret(list_arrets_data)
            list_raisons = Database.get_raison(self.start, self.end)
            print(list_raisons)
            self.add_raisons_to_arret(list_raisons, self.dic_arret)
            self.arrets = self.convert_dic_to_array(self.dic_arret)
            if self.arrets:
                self.get_arret_stat(ts)
            return True, list_new_arret
        except:
            return False, []

    @staticmethod
    def get_live_stat(speeds, ts):

        def get_start_and_end(ts, moment):
            vendredi = timestamp_to_day(ts) == "vendredi"
            start = DEBUT_PROD_MATIN
            mid = FIN_PROD_MATIN_VENDREDI if vendredi else FIN_PROD_MATIN
            end = FIN_PROD_SOIR_VENDREDI if vendredi else FIN_PROD_SOIR
            if moment == "matin":
                end = mid
            if moment == "soir":
                start = mid
            return start, end

        def get_metrage(ts, speeds, moment):
            data_ts = get_start_and_end(ts, moment)
            start_ts = timestamp_at_time(ts, hours=data_ts[0])
            end_ts = timestamp_at_time(ts, hours=data_ts[1])

            def value_is_in_period(value):
                return start_ts <= value[0] <= end_ts

            speeds_moment = [v[1] for v in list(filter(value_is_in_period, speeds))]
            return speeds_moment

        speeds_matin = get_metrage(ts, speeds, "matin")
        metrage_matin = sum(speeds_matin) / 60
        speeds_soir = get_metrage(ts, speeds, "soir")
        metrage_soir = sum(speeds_soir) / 60
        return metrage_matin, metrage_soir

    def get_arret_stat(self, ts):
        self.arret_time_matin = 0
        self.imprevu_arret_time_matin = 0
        self.arret_time_soir = 0
        self.imprevu_arret_time_soir = 0
        vendredi = timestamp_to_day(ts) == "vendredi"
        time_change_of_team = FIN_PROD_MATIN_VENDREDI if vendredi else FIN_PROD_MATIN
        ts_change_of_team = timestamp_at_time(ts, hours=time_change_of_team)
        arrets = self.arrets
        for arret in arrets:
            start_arret = arret[0]
            end_arret = arret[1]
            arret_delay = end_arret - start_arret
            if start_arret <= ts_change_of_team > end_arret:
                self.arret_time_matin += arret_delay
            elif start_arret <= ts_change_of_team < end_arret:
                self.arret_time_matin += ts_change_of_team - start_arret
                self.arret_time_soir += end_arret - ts_change_of_team
            else:
                self.arret_time_soir += arret_delay
            if arret[2]:
                first_raison = arret[2][0]
                if first_raison.type == "Imprévu":
                    if start_arret <= ts_change_of_team > end_arret:
                        self.imprevu_arret_time_matin += arret_delay
                    elif start_arret <= ts_change_of_team < end_arret:
                        self.imprevu_arret_time_matin += ts_change_of_team - start_arret
                        self.imprevu_arret_time_soir += end_arret - ts_change_of_team
                    else:
                        self.imprevu_arret_time_soir += arret_delay

    @staticmethod
    def convert_dic_to_array(dic):
        """
        Convertie un dictionnaire (clé:start_arret, valeur:Arret) en un tableau de [start, end]
        :param dic: Dictionnaire d'arrêt
        :return: Un tableau de data d'arret [start, end]
        """
        # Initialisation du tableau à retourner
        array = []
        # Parcours les valeurs du dictionnaire
        for value in dic.items():
            # value[1] est l'models Arret du dictionnaire
            # Assigne les valeurs de l'arrêt dans tab
            start = value[1].start
            end = value[1].end
            raisons = value[1].raisons
            tab = [start, end, raisons]
            # Ajoute tab au tableau à retourner
            array.append(tab)
        return array

    def add_raisons_to_arret(self, list_raisons, dic_arret):
        """
        Ajoute les raisons enregistrées dans la base de donnée a son arret associé
        :param list_raisons: Liste des raisons que l'on récupère de la base de donnée
        :param dic_arret: Dictionnaire des arrêts mis a jours précedemment
        """
        # On parcour les raisons de la base de donnée
        for raison in list_raisons:
            start_raison = raison[1]
            id_raison = raison[0]
            # Test si le start de la raison correspond au start d'un arret
            arret_object = self.check_start_raison(dic_arret, start_raison)
            if arret_object:
                # Test si la raison est déja renseigné dans l'models Arret
                if self.check_id_raison(arret_object, id_raison):
                    # Si oui on ne fait rien
                    continue
                else:
                    # Sinon on crée un models raison est on l'insert dans le tableau de raison de l'arret
                    from models.raison import Raison
                    raison_object = Raison(raison)
                    arret_object.raisons.append(raison_object)
                arret_object.raisons = arret_object.raison_store(arret_object.raisons)

    @staticmethod
    def check_start_raison(dic_arret, start):
        """
        Permet d'identifer un arret dans un dictionnaire d'arret avec la valeur start
        :param dic_arret: Dictionnaire d'arret
        :param start: Valeur du start arret recherché
        :return: l'models arret trouvé ou False
        """
        for value in dic_arret.items():
            start_arret = value[0]
            if start_arret == start:
                return value[1]
        return False

    @staticmethod
    def check_id_raison(arret_object, id):
        """
        Permet de checker si une raison est déja présente dans le tableau de raison d'un arret
        :param arret_object: Object arret ou l'on test
        :param id: Id que l'on recherche dans l'arret
        :return: True si la raison est présente, False si on ne l'a trouve pas
        """
        list_raisons = arret_object.raisons
        for raison in list_raisons:
            raison_id = raison.id
            if raison_id == id:
                return True
        return False

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
            # Sinon on ajoute un models Arret au dictionnaire avec les datas de la base de donnée
            else:
                from models.arret import Arret
                object_arret = Arret(arret_database)
                self.dic_arret[start_arret] = object_arret

    def update_dic_arret(self, list_arrets_data):
        """
        S'occupe de créer un nouvelle arret en base de donnée si besoin
        Met a jour la fin d'un Arret contenue dans le dictionnaire si besoin
        :param list_arrets_data: Un tableau de tuple (start, end) définit par les vitesses de la base de donnée
        """
        list_new_arret = []
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
            # Sinon on ajoute un models Arret au dictionnaire
            # On utilise les datas définit par les vitesses de la base de donnée
            else:
                from models.arret import Arret
                arret_data = [start_arret, end_arret]
                object_arret = Arret(arret_data)
                self.dic_arret[start_arret] = object_arret
                list_new_arret.append(start_arret)
        return list_new_arret

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
        start = DEBUT_PROD_MATIN
        # La fin de journée est 22h sauf le vendredi 20h
        end = FIN_PROD_SOIR_VENDREDI if vendredi else FIN_PROD_SOIR
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
                if 0 <= value[1] <= VITESSE_LIMITE_ASSIMILATION_ARRET:
                    # Si on est pas déja dans un arrêt on définit le début de l'arrêt
                    if not speed_is_0:
                        start = value[0]
                    end = value[0]
                    speed_is_0 = True
                # Si on vient de sortir d'un arrêt on ajoute l'arrêt à la liste d'arrêts
                elif speed_is_0:
                    if start != end:
                        arrets.append((start, end))
                    start = 0
                    end = 0
                    speed_is_0 = False
                else:
                    continue
        # Si on sort de la boucle avec un arrêt en cours on ajoute le dernier arrêt à la liste d'arrêts
        if speed_is_0 and start != end:
            arrets.append((start, end))
        return arrets

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
        last_data = 0
        if self.data:
            for data in self.data:
                if data[1] >= 0:
                    last_data = data[1]
            return last_data
        return None
