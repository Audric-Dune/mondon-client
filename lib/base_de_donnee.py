# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from time import sleep

from constants.param import DATABASE_LOCATION
from lib.logger import logger


class Database:
    """
    S'occupe de maintenir une connexion à une base de données SQLite3 et d'exécuter des requêtes
    """
    MAX_ATTEMPT_ON_ERROR = 3  # Nombre de fois que l'on réessaye d'exécuter une requête SQL avant
                              # d'abandonner en cas d'erreurs qui n'ont rien à voir avec la requête
                              # elle même. Par exemple, si la base de données est vérouillée parce
                              # que un autre programme essaye d'y accéder. Ou si la connexion à la
                              # base de données est cassée pour une raison inconnue.
    SLEEP_ON_ERROR_MS = 10  # Temps d'attent en millisecondes en cas d'erreur avant de réessayer.

    def __init__(self, database_location):
        """
        Crée une nouvelle instance de `Database` et établit une connexion à la base de données.
        :param database_location: Chemin du fichier contenant la base de données
        """
        self.database_location = database_location
        self._init_db_connection()

    @classmethod
    def _create_database_connection(cls):
        """
        Crée une nouvelle connexion à la base de données.
        :return: Une nouvelle connexion à la base de données
        """
        logger.log("DATABASE", "Connection à la base de données {}".format(DATABASE_LOCATION))
        conn = sqlite3.connect(DATABASE_LOCATION)
        return conn

    @classmethod
    def _run_query(cls, query, args):
        """
        Exécute une requête sur la base de données
        :param query: Requête SQL à exécuter
        :param args: Paramètre de la requête à exécuter
        :return: Un array avec le résultat de la requête.
                 Retourne un tableau vide pour les CREATE et INSERT
        """
        logger.log("DATABASE", "Requête: {} - Paramêtres: {}".format(query, args))
        data = None
        attempt = 0
        conn = cls._create_database_connection()

        while attempt < Database.MAX_ATTEMPT_ON_ERROR:
            if attempt > 0:
                sleep(Database.SLEEP_ON_ERROR_MS / 1000)  # Pause entre 2 tentatives
                logger.log("DATABASE", "(Tentative #{}) Requête: {} - Paramêtres: {}"
                           .format(attempt + 1, query, args))
            try:
                cursor = conn.cursor()
                cursor.execute(query, args)
                conn.commit()
                data = cursor.fetchall()
                break
            except sqlite3.OperationalError as e:
                # OperationalError veut généralement dire que la base de données est locked ou
                # de manière générale qu'une erreur s'est produite lors de la lecture du fichier
                # où la base de données est stockée.
                logger.log("DATABASE", "OperationalError: {}".format(e))
                attempt += 1
            except sqlite3.DatabaseError as e:
                if e.__class__.__name__ == "DatabaseError":
                    # DatabaseError veut généralement dire qu'une erreur grave s'est produite.
                    # En générale, cela veut dire que la base de données est corrompue et l'on ne
                    # peut pas faire grand chose. On essaye quand même de s'en sortir en recréant
                    # la connexion à la base de données.
                    logger.log("DATABASE", "DatabaseError: {}".format(e))
                    attempt += 1
                    conn = cls._create_database_connection()
                # Si l'exception n'est pas directement une DatabaseError (ex: une sous class de
                # DatabaseError comme IntegrityError), on abandonne directement.
                else:
                    raise e

        # Dans le cas où on a consommé tous les essais possible, on génère une erreur
        if attempt >= Database.MAX_ATTEMPT_ON_ERROR:
            raise Exception("Abandon de la requête {} avec les paramètres {}. Une erreur s'est"
                            "produite à chacun des {} essais"
                            .format(query, args, Database.MAX_ATTEMPT_ON_ERROR))

        return data

    @classmethod
    def get_speeds(cls, start_time, end_time):
        """
        Récupère les vitesses entre une plage de timestamp dans l'ordre chronologique
        :param start_time: Timestamp minimum des vitesses
        :param end_time: Timestamp maximum des vitesses
        :return: Une liste de tuples (timestamp, speed)
        """
        query = "SELECT time, speed " \
                "FROM mondon_speed " \
                "WHERE time > ? AND time <= ? AND speed IS NOT NULL " \
                "ORDER BY time"\
            .format(start_time=start_time, end_time=end_time)
        speeds = cls._run_query(query, (start_time, end_time))
        return speeds

    @classmethod
    def get_arret(cls, start_time, end_time):
        """
        Récupère les arrêts en base de donnée compris entre une plage de timestamp dans l'ordre chronologique
        :param start_time: Timestamp minimum de l'arrêt
        :param end_time: Timestamp maximum de l'arrêt
        :return: Une liste
        """
        query = "SELECT start, end " \
                "FROM mondon_arret " \
                "WHERE start > ? AND start <= ?" \
                "ORDER BY start"\
            .format(start_time=start_time, end_time=end_time)
        arrets = cls._run_query(query, (start_time, end_time))
        return arrets

    @classmethod
    def create_arret(cls, start_arret, end_arret):
        """
        Ajoute l'arrêt en base donnée
        :param start_arret: Timestamp début de l'arrêt
        :param end_arret: Timestamp fin de l'arrêt
        """
        try:
            cls._run_query("INSERT INTO mondon_arret VALUES (?, ?)", (start_arret, end_arret))
        except sqlite3.IntegrityError as e:
            # IntegrityError veut dire que l'on essaye d'insérer une vitesse avec un timestamp
            # qui existe déjà dans la base de données.
            # Dans ce cas, on considère que cette valeur n'a pas besoin d'être insérée et on
            # ignore l'exception.
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

    @classmethod
    def update_arret(cls, start_arret, end_arret):
        """
        Met à jour un arret
        :param start_arret: Début de l'arrêt (clé pour retrouver l'arret en base de donnée)
        :param end_arret: Fin de l'arret
        """
        query = "UPDATE mondon_arret " \
                "SET end = ?" \
                "WHERE start = ?" \
            .format(end_arret, start_arret)
        try:
            cls._run_query(query, (end_arret, start_arret))
        except sqlite3.IntegrityError as e:
            # IntegrityError veut dire que l'on essaye d'insérer une vitesse avec un timestamp
            # qui existe déjà dans la base de données.
            # Dans ce cas, on considère que cette valeur n'a pas besoin d'être insérée et on
            # ignore l'exception.
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

    @classmethod
    def get_raison(cls, start_time, end_time):
        """
        Récupère les raisons d'arret en base de donnée compris entre une plage de timestamp dans l'ordre chronologique
        :param start_time: Timestamp minimum de l'arrêt
        :param end_time: Timestamp maximum de l'arrêt
        :return: Une liste de raisons d'arret
        """
        query = "SELECT id, start_arret, type_arret, raison_arret, duree " \
                "FROM mondon_raison_arret " \
                "WHERE start_arret > ? AND start_arret <= ?" \
                "ORDER BY start_arret"\
            .format(start_time=start_time, end_time=end_time)
        raisons = cls._run_query(query, (start_time, end_time))
        return raisons

    @classmethod
    def create_raison_arret(cls, id, start_arret, type_arret, raison_arret, duree=None):
        query = "INSERT INTO mondon_raison_arret VALUES (?, ?, ?, ?, ?)"\
            .format(id=id,
                    start_arret=start_arret,
                    type_arret=type_arret,
                    raison_arret=raison_arret,
                    duree=duree)
        try:
            cls._run_query(query, (id, start_arret, type_arret, raison_arret, duree))
        except sqlite3.IntegrityError as e:
            # IntegrityError veut dire que l'on essaye d'insérer une vitesse avec un timestamp
            # qui existe déjà dans la base de données.
            # Dans ce cas, on considère que cette valeur n'a pas besoin d'être insérée et on
            # ignore l'exception.
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

    @classmethod
    def get_dechet(cls, start_time, end_time):
        """
        Récupère les déchets en base de donnée compris entre une plage de timestamp dans l'ordre chronologique
        :param start_time: Timestamp minimum du déchet
        :param end_time: Timestamp maximum du déhet
        :return: Une liste
        """
        query = "SELECT id, arret_start, type, masse, piste, couleur, grammage_papier, grammage_polypro " \
                "FROM mondon_dechet " \
                "WHERE arret_start > ? AND arret_start <= ?" \
                "ORDER BY arret_start"\
            .format(start_time=start_time, end_time=end_time)
        dechets = cls._run_query(query, (start_time, end_time))
        return dechets

