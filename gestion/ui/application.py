# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from random import randint

from gestion.window.main_window import MainWindow
from commun.stores.bobine_fille_store import bobine_filles_store
from commun.model.bobine_filles import BobineFille
from commun.stores.bobine_mere_store import bobine_meres_store
from commun.model.bobine_mere import BobineMere
import xlrd


class Application(QApplication):

    def __init__(self, argv=None):
        if argv is None:
            argv = []
        super(Application, self).__init__(argv)
        self.read_xlsm()
        self.main_window = MainWindow()
        self.main_window.show()

    def read_xlsm(self):
        wb = xlrd.open_workbook('C:/Users\dessinateur3\Desktop\github\Etude stock bobine V5 MASTER 18-02-23.xlsm')
        for sheet in wb.sheets():
            if sheet.name == "Liste bobine":
                start_ligne = 20
                code = 0
                current_ligne = start_ligne
                while current_ligne < sheet.nrows:
                    if sheet.cell_value(current_ligne, 1) == "":
                        break
                    else:
                        color = self.get_color(sheet.cell_value(current_ligne, 8))
                        gr = self.get_gr(sheet.cell_value(current_ligne, 8))
                        alerte = self.is_alerte(wb, sheet.cell_value(current_ligne, 3), sheet.cell_value(current_ligne, 6))
                        bobine_fille = BobineFille(code=code,
                                                   color=color,
                                                   laize=sheet.cell_value(current_ligne, 9),
                                                   gr=gr,
                                                   lenght=sheet.cell_value(current_ligne, 26),
                                                   pose=randint(1, 7),
                                                   alerte=alerte)
                        print(bobine_fille)
                        bobine_filles_store.add_bobine(bobine_fille)
                    current_ligne += 1
                    code += 1
            if sheet.name == "TYPE BOBINE MERE":
                start_ligne = 1
                current_ligne = start_ligne
                while current_ligne < sheet.nrows:
                    if sheet.cell_value(current_ligne, 1) == "":
                        break
                    else:
                        code = sheet.cell_value(current_ligne, 3)
                        color = sheet.cell_value(current_ligne, 1)
                        gr = self.get_gr_bobine_mere(gr=sheet.cell_value(current_ligne, 5))
                        bobine_mere = BobineMere(code=code,
                                                 color=color,
                                                 laize=sheet.cell_value(current_ligne, 0),
                                                 gr=gr,
                                                 lenght=sheet.cell_value(current_ligne, 6))
                        print(bobine_mere)
                        bobine_meres_store.add_bobine(bobine_mere)
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
    def get_gr_bobine_mere(gr):
        if gr != "":
            gr += "g"
            return gr
        else:
            return "CX"


app = Application()
