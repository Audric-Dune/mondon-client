# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from time import sleep

from commun.constants.param import DATABASE_LOCATION
from commun.lib.logger import logger
from commun.constants.param import DEBUT_PROD_MATIN,\
    FIN_PROD_MATIN_VENDREDI,\
    FIN_PROD_MATIN,\
    FIN_PROD_SOIR,\
    FIN_PROD_SOIR_VENDREDI
from commun.utils.day import is_vendredi


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

    @classmethod
    def create_database_connection(cls):
        """
        Crée une nouvelle connexion à la base de données.
        :return: Une nouvelle connexion à la base de données
        """
        logger.log("DATABASE", "Connection à la base de données {}".format(DATABASE_LOCATION))
        conn = sqlite3.connect(DATABASE_LOCATION)
        return conn

    @classmethod
    def run_query(cls, query, args):
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
        conn = cls.create_database_connection()

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
                    conn = cls.create_database_connection()
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
        speeds = cls.run_query(query, (start_time, end_time))
        return speeds

    @classmethod
    def get_all_jour_metrages(cls):
        """
        Récupère tout les jours ou le metrage est enregistree dans l'ordre chronologique
        :return: Une liste de tuples (timestamp, speed)
        """
        query = "SELECT ts_jour " \
                "FROM mondon_metrage " \
                "ORDER BY ts_jour"
        jour_metrage = cls.run_query(query, ())
        return jour_metrage

    @classmethod
    def get_metrages(cls, start_time, end_time):
        """
        Récupère les metrages des jours compris entre start et end
        :param start_time: Timestamp minimum (inclus)
        :param end_time: Timestamp maximum (exclus)
        :return: Une liste
        """
        query = "SELECT ts_jour, metrage_matin, metrage_soir " \
                "FROM mondon_metrage " \
                "WHERE ts_jour >= ? AND ts_jour < ? " \
                "ORDER BY ts_jour"\
            .format(start_time=start_time, end_time=end_time)
        speeds = cls.run_query(query, (start_time, end_time))
        return speeds

    @classmethod
    def get_metrages_for_one_day(cls, start_time):
        """
        Récupère les metrages des jours compris entre start et end
        :param start_time: Timestamp minimum (inclus)
        :return: Une liste
        """
        query = "SELECT metrage_matin, metrage_soir " \
                "FROM mondon_metrage " \
                "WHERE ts_jour = ? "\
            .format(start_time=start_time)
        metrages = cls.run_query(query, (start_time,))
        return metrages

    @classmethod
    def insert_jour_metrages(cls, ts_jour, metrage_matin, metrage_soir):
        """
        Ajoute les metrages matin et soir d'un jour en base de donnee
        :param ts_jour: timestamp du debut du jour renseigne
        :param metrage_matin: la somme du metrage pour l'equipe du matin
        :param metrage_soir: la somme du metrage pour l'equipe du soir
        """
        try:
            cls.run_query("INSERT INTO mondon_metrage VALUES (?, ?, ?)", (ts_jour, metrage_matin, metrage_soir))
        except sqlite3.IntegrityError as e:
            # IntegrityError veut dire que l'on essaye d'insérer une vitesse avec un timestamp
            # qui existe déjà dans la base de données.
            # Dans ce cas, on considère que cette valeur n'a pas besoin d'être insérée et on
            # ignore l'exception.
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

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
                "WHERE start >= ? AND start <= ? " \
                "ORDER BY start"\
            .format(start_time=start_time, end_time=end_time)
        arrets = cls.run_query(query, (start_time, end_time))
        return arrets

    @classmethod
    def create_arret(cls, start_arret, end_arret):
        """
        Ajoute l'arrêt en base donnée
        :param start_arret: Timestamp début de l'arrêt
        :param end_arret: Timestamp fin de l'arrêt
        """
        try:
            cls.run_query("INSERT INTO mondon_arret VALUES (?, ?)", (start_arret, end_arret))
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
                "SET end = ? " \
                "WHERE start = ?" \
            .format(end_arret, start_arret)
        try:
            cls.run_query(query, (end_arret, start_arret))
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
        query = "SELECT id, start_arret, type_arret, raison_arret, primaire " \
                "FROM mondon_raison_arret " \
                "WHERE start_arret >= ? AND start_arret <= ? " \
                "ORDER BY start_arret"\
            .format(start_time=start_time, end_time=end_time)
        raisons = cls.run_query(query, (start_time, end_time))
        return raisons

    @classmethod
    def update_to_raison_primaire(cls, _id, primaire):
        """
        Update une raison pour la rendre primaire
        :param _id: L'id de la raison
        :param primaire: 1 si la raison est primaire
        """
        query = "UPDATE mondon_raison_arret " \
                "SET primaire = ? " \
                "WHERE id = ?" \
            .format(primaire, _id)
        try:
            cls.run_query(query, (primaire, _id))
        except sqlite3.IntegrityError as e:
            # IntegrityError veut dire que l'on essaye d'insérer une vitesse avec un timestamp
            # qui existe déjà dans la base de données.
            # Dans ce cas, on considère que cette valeur n'a pas besoin d'être insérée et on
            # ignore l'exception.
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

    @classmethod
    def create_raison_arret(cls, _id, start_arret, type_arret, raison_arret, primaire=0):
        query = "INSERT INTO mondon_raison_arret VALUES (?, ?, ?, ?, ?)"\
            .format(id=_id,
                    start_arret=start_arret,
                    type_arret=type_arret,
                    raison_arret=raison_arret,
                    prioritaire=primaire)
        try:
            cls.run_query(query, (_id, start_arret, type_arret, raison_arret, primaire))
        except sqlite3.IntegrityError as e:
            # IntegrityError veut dire que l'on essaye d'insérer une vitesse avec un timestamp
            # qui existe déjà dans la base de données.
            # Dans ce cas, on considère que cette valeur n'a pas besoin d'être insérée et on
            # ignore l'exception.
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

    @classmethod
    def delete_raison_arret(cls, _id):
        query = "DELETE FROM mondon_raison_arret WHERE id = ?"\
            .format(id=_id)
        try:
            cls.run_query(query, (_id,))
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
        query = "SELECT id, start_arret, type, masse, piste, couleur, grammage_papier, grammage_polypro " \
                "FROM mondon_dechet " \
                "WHERE start_arret > ? AND arret_start <= ? " \
                "ORDER BY start_arret"\
            .format(start_time=start_time, end_time=end_time)
        dechets = cls.run_query(query, (start_time, end_time))
        return dechets

    @classmethod
    def get_team_gestion(cls):
        """
        Récupère les donnée de gestion des équipes
        :return: Une liste
        """
        query = "SELECT ts, debut_prod, equipe_matin, conducteur_matin, aide_matin, heure_matin," \
                " equipe_soir, conducteur_soir, aide_soir, heure_soir, ferier " \
                "FROM mondon_equipe " \
                "ORDER BY ts"\
            .format()
        data_team = cls.run_query(query, ())
        return data_team

    @classmethod
    def add_defaut_day(cls, start_day):
        """
        Récupère les donnée de gestion des équipes
        :return: Une liste
        """
        equipe_matin = 1
        conducteur_matin = "Fred"
        aide_matin = "Jean-Luc"
        heure_matin = FIN_PROD_MATIN_VENDREDI - DEBUT_PROD_MATIN if is_vendredi(start_day) else FIN_PROD_MATIN - DEBUT_PROD_MATIN
        equipe_soir = 1
        conducteur_soir = "Fred2"
        aide_soir = "Cyril"
        heure_soir = FIN_PROD_SOIR_VENDREDI - FIN_PROD_MATIN_VENDREDI if is_vendredi(start_day) else FIN_PROD_SOIR - FIN_PROD_MATIN
        ferier = 0
        query = "INSERT INTO mondon_equipe VALUES(?,?,?,?,?,?,?,?,?,?,?)".format(start_day,
                                                                                 DEBUT_PROD_MATIN,
                                                                                 equipe_matin,
                                                                                 conducteur_matin,
                                                                                 aide_matin,
                                                                                 heure_matin,
                                                                                 equipe_soir,
                                                                                 conducteur_soir,
                                                                                 aide_soir,
                                                                                 heure_soir, ferier)
        try:
            pass
        except sqlite3.IntegrityError as e:
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

    @classmethod
    def get_refente(cls):
        query = "SELECT id, id_perfo, dec, laize1, laize2, laize3," \
                " laize4, laize5, laize6, laize7, chute " \
                "FROM mondon_refente " \
            .format()
        data_refente = cls.run_query(query, ())
        return data_refente

    @classmethod
    def get_perfo(cls):
        query = "SELECT id, dec_init, cale1, bague1, cale2, bague2, cale3, bague3, cale4, bague4," \
                "cale5, bague5, cale6, bague6, cale7, bague7 " \
                "FROM mondon_perfo " \
            .format()
        data_perfo = cls.run_query(query, ())
        return data_perfo

    @classmethod
    def create_plan_prod(cls, p_id, start, refente, bobine_papier, code_bobines_selected, longueur, tours, bobine_poly,
                         encrier_1, encrier_2, encrier_3, code_data_reglages):
        query = "INSERT INTO mondon_plan_prod (refente,bobine_papier,start,p_id,code_bobines_selected," \
                "longueur,tours,bobine_poly,encrier_1,encrier_2,encrier_3,code_data_reglages) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(refente, bobine_papier, start, p_id,
                                                                     code_bobines_selected, longueur, tours,
                                                                     bobine_poly, encrier_1, encrier_2, encrier_3,
                                                                     code_data_reglages)
        try:
            cls.run_query(query, (refente, bobine_papier, start, p_id, code_bobines_selected, longueur, tours,
                                  bobine_poly, encrier_1, encrier_2, encrier_3, code_data_reglages))
        except sqlite3.IntegrityError as e:
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

    @classmethod
    def get_plan_prod(cls):
        query = "SELECT p_id, start, tours, longueur, bobine_papier, refente, code_bobines_selected, bobine_poly, " \
                "encrier_1, encrier_2, encrier_3, code_data_reglages " \
                "FROM mondon_plan_prod ORDER BY start"
        data_plan_prod = cls.run_query(query, ())
        return data_plan_prod

    @classmethod
    def update_plan_prod(cls, p_id, start, refente, bobine_papier, code_bobines_selected, longueur, tours, bobine_poly,
                         encrier_1, encrier_2, encrier_3, code_data_reglages):
        query = "UPDATE mondon_plan_prod " \
                "SET start = ?, refente = ?, bobine_papier = ?, code_bobines_selected = ?, longueur = ?, tours = ?," \
                "bobine_poly = ?, encrier_1 = ?, encrier_2 = ?, encrier_3 = ?, code_data_reglages = ? WHERE p_id = ? " \
            .format(start, refente, bobine_papier, code_bobines_selected, longueur, tours, bobine_poly, encrier_1,
                    encrier_2, encrier_3, code_data_reglages, p_id)
        try:
            cls.run_query(query, (start, refente, bobine_papier, code_bobines_selected, longueur, tours,
                                  bobine_poly, encrier_1, encrier_2, encrier_3, code_data_reglages, p_id))
        except sqlite3.IntegrityError as e:
            # IntegrityError veut dire que l'on essaye d'insérer une vitesse avec un timestamp
            # qui existe déjà dans la base de données.
            # Dans ce cas, on considère que cette valeur n'a pas besoin d'être insérée et on
            # ignore l'exception.
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

    @classmethod
    def create_event_prod(cls, start, end, p_type, info=None, ensemble=None):
        query = "INSERT INTO mondon_event (type,start,end,info, ensemble) " \
                "VALUES (?, ?, ?, ?, ?)".format(p_type, start, end, info, ensemble)
        try:
            cls.run_query(query, (p_type, start, end, info, ensemble))
        except sqlite3.IntegrityError as e:
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

    @classmethod
    def get_event_prod(cls):
        query = "SELECT id, type, start, end, info, ensemble FROM mondon_event"
        data_event_prod = cls.run_query(query, ())
        return data_event_prod

    @classmethod
    def get_last_id_plan_prod(cls):
        query = "SELECT id FROM mondon_plan_prod ORDER BY id DESC LIMIT 1"
        last_id = cls.run_query(query, ())
        return last_id[0][0]

    @classmethod
    def delete_event_prod(cls, p_id):
        query = "DELETE FROM mondon_event " \
                "WHERE id = ? ".format(p_id)
        try:
            cls.run_query(query, (p_id,))
        except sqlite3.IntegrityError as e:
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

    @classmethod
    def delete_plan_prod(cls, p_id):
        query = "DELETE FROM mondon_plan_prod " \
                "WHERE p_id = ? ".format(p_id)
        try:
            cls.run_query(query, (p_id,))
        except sqlite3.IntegrityError as e:
            logger.log("DATABASE", "(Ignorée) IntegrityError: {}".format(e))
            pass

