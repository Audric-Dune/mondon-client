# !/usr/bin/env python
# -*- coding: utf-8 -*-

#  Importation du module de gestion des base de donnée
import sqlite3
import time
from object.logger import logger

#  Object de dialogue programme/base de donnée
class DataBase(object):

    #  Fonction qui execute la requête et retourne le résultat
    @classmethod
    def run_query(cls, query):
        #  Ouverture de la connection à la base de donnée
        conn = sqlite3.connect("/Users/audricperrin/Desktop/Boulot/mondon.db")
        #  Container de requête sql
        cursor = conn.cursor()
        #  Ajout requête au container
        cursor.execute(query)
        #  Envoi le container à la base de donnée
        conn.commit()
        #  Récupère le résultat
        data = cursor.fetchall()
        # Fermeture connection
        conn.close()
        return data

    #  Fonction d'insertion d'une valeur dans la base de donnée
    @classmethod
    def insert_speed(cls, value):
        ts = int(round(time.time() * 1000))
        query = "INSERT INTO mondon_speed VALUES ({time}, {speed})".format(time=ts, speed=value)
        cls.run_query(query)

    #  Fonction de récupération de valeur comprise entre une plage de temps depuis la base de donnée
    @classmethod
    def get_speeds(cls, start_time, end_time):
        query = "SELECT time, speed " \
                "FROM mondon_speed " \
                "WHERE time > {start_time} AND time <= {end_time} AND speed IS NOT NULL " \
                "ORDER BY time"\
            .format(start_time=start_time, end_time=end_time)
        from datetime import datetime
        speeds = cls.run_query(query)
        return speeds
