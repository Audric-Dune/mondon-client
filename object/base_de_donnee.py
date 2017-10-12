# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from time import sleep

from object.logger import logger


class Database:
    """
    S'occupe de maintenir une connexion à une base de données SQLite3 et d'exécuter des requêtes
    """
    DATABASE_LOCATION = '../mondon.db'  # Où le fichier SQLite de la base de données est stocké.
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
        logger.log("DATABASE", "Connection à la base de données {}".format(cls.DATABASE_LOCATION))
        conn = sqlite3.connect(cls.DATABASE_LOCATION)
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
