# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from random import randint

from gestion.window.main_window import MainWindow
from commun.lib. base_de_donnee import Database
from commun.stores.bobine_fille_store import bobine_fille_store
from commun.model.bobine_filles import BobineFille
from commun.stores.bobine_poly_store import bobine_poly_store
from commun.stores.bobine_papier_store import bobine_papier_store
from commun.stores.refente_store import refente_store
from commun.model.bobine_mere import BobineMere
from commun.model.refente import Refente
import xlrd


class Application(QApplication):

    def __init__(self, argv=None):
        if argv is None:
            argv = []
        super(Application, self).__init__(argv)
        self.main_window = None
        self.read_xlsm()
        self.init_refente_store()
        self.init_ui()

    def init_ui(self):
        self.main_window = MainWindow()
        self.main_window.show()

    @staticmethod
    def init_refente_store():
        data_refentes = Database.get_refente()
        for data_refente in data_refentes:
            new_refente = Refente(code=data_refente[0],
                                  code_perfo=data_refente[1],
                                  dec=data_refente[2],
                                  laize1=data_refente[3],
                                  laize2=data_refente[4],
                                  laize3=data_refente[5],
                                  laize4=data_refente[6],
                                  laize5=data_refente[7],
                                  laize6=data_refente[8],
                                  laize7=data_refente[9])
            refente_store.add_refente(new_refente)
        print(refente_store)

    def read_xlsm(self):
        wb = xlrd.open_workbook('C:/Users\Castor\Desktop\github\Etude stock bobine V5 MASTER 18-02-23.xlsm')
        for sheet in wb.sheets():
            if sheet.name == "Liste bobine":
                start_ligne = 20
                current_ligne = start_ligne
                while current_ligne < sheet.nrows:
                    if sheet.cell_value(current_ligne, 1) == "":
                        break
                    else:
                        color = self.get_color(sheet.cell_value(current_ligne, 8))
                        gr = self.get_gr(sheet.cell_value(current_ligne, 8))
                        alerte = self.is_alerte(wb, sheet.cell_value(current_ligne, 3),
                                                sheet.cell_value(current_ligne, 6))
                        sommeil = self.is_sommeil(sheet.cell_value(current_ligne, 2))
                        bobine_fille = BobineFille(code=sheet.cell_value(current_ligne, 0),
                                                   color=color,
                                                   laize=sheet.cell_value(current_ligne, 9),
                                                   gr=gr,
                                                   lenght=sheet.cell_value(current_ligne, 26),
                                                   pose=randint(1, 7),
                                                   alerte=alerte,
                                                   sommeil=sommeil)
                        print(bobine_fille)
                        bobine_fille_store.add_bobine(bobine_fille)
                    current_ligne += 1
            if sheet.name == "TYPE BOBINE MERE":
                start_ligne = 1
                current_ligne = start_ligne
                while current_ligne < sheet.nrows:
                    if sheet.cell_value(current_ligne, 1) == "":
                        break
                    else:
                        code = sheet.cell_value(current_ligne, 3)
                        color = sheet.cell_value(current_ligne, 1)
                        gr = self.get_gr_bobine_mere(gr=sheet.cell_value(current_ligne, 5),
                                                     color=sheet.cell_value(current_ligne, 1))
                        bobine_mere = BobineMere(code=code,
                                                 color=color,
                                                 laize=sheet.cell_value(current_ligne, 0),
                                                 gr=gr,
                                                 lenght=sheet.cell_value(current_ligne, 6))
                        print(bobine_mere)
                        if color == "Poly":
                            bobine_poly_store.add_bobine(bobine_mere)
                        else:
                            bobine_papier_store.add_bobine(bobine_mere)
                    current_ligne += 1

    @staticmethod
    def get_color(string):
        string_list = list(string)
        color = ""
        for character in string_list:
            if character == " ":
                break
            else:
                color += character
        return color

    @staticmethod
    def get_gr(string):
        string_list = list(string)
        gr = ""
        start_gr = False
        for character in string_list:
            if character == " ":
                start_gr = True
            if start_gr and character != " " and character != "G":
                gr += character
        if gr != "CX":
            gr += "g"
        return gr if start_gr else "35g"

    @staticmethod
    def is_alerte(wb, vente_annuel, stock_a_therme):
        for sheet in wb.sheets():
            if sheet.name == "Alerte Prod":
                start_ligne = 1
                current_ligne = start_ligne
                while current_ligne < sheet.nrows:
                    if sheet.cell_value(current_ligne, 1) == "":
                        break
                    elif sheet.cell_value(current_ligne, 0) <= vente_annuel <= sheet.cell_value(current_ligne, 1):
                        if stock_a_therme <= sheet.cell_value(current_ligne, 2):
                            return True
                    current_ligne += 1
                return False

    @staticmethod
    def get_gr_bobine_mere(gr, color):
        if gr != "" and color != "POLY":
            gr += "g"
            return gr
        elif color == "POLY":
            return "20µ"
        else:
            return "CX"

    @staticmethod
    def is_sommeil(sommeil):
        if sommeil == "Sommeil":
            return True
        else:
            return False


app = Application()
