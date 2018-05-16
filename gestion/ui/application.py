# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication

from gestion.ui.window.main_window import MainWindow
from commun.lib. base_de_donnee import Database
from commun.stores.bobine_fille_store import bobine_fille_store
from commun.stores.bobine_poly_store import bobine_poly_store
from commun.stores.bobine_papier_store import bobine_papier_store
from commun.stores.refente_store import refente_store
from commun.stores.perfo_store import perfo_store
from commun.stores.cliche_store import cliche_store
from commun.model.bobine_fille import BobineFille
from commun.model.cliche import Cliche
from commun.model.bobine_mere import BobineMere
from commun.model.refente import Refente
from commun.model.perfo import Perfo
import xlrd


# List des dossiers où il est possible que les fichiers excels se trouvent.
DOSSIERS_POTENTIELS = [
    'C:/Users\\dessinateur3\\Desktop\\github\\',
    'C:/Users\\Castor\\Desktop\\github\\',
    '/Users/audricperrin/Desktop/github/',
    '../', # dossier parent du code/executable
]


def open_xls(file_name):
    for directory in DOSSIERS_POTENTIELS:
        try:
            return xlrd.open_workbook(directory + file_name)
        except FileNotFoundError:
            continue
    return None


class Application(QApplication):

    def __init__(self, argv=None):
        if argv is None:
            argv = []
        super(Application, self).__init__(argv)
        self.main_window = None
        self.read_xls()
        self.read_xlsm()
        self.init_refente_store()
        self.init_perfo_store()
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

    @staticmethod
    def init_perfo_store():
        data_perfos = Database.get_perfo()
        for data_perfo in data_perfos:
            new_perfo = Perfo(code=data_perfo[0],
                              dec_init=data_perfo[1],
                              cale1=data_perfo[2],
                              bague1=data_perfo[3],
                              cale2=data_perfo[4],
                              bague2=data_perfo[5],
                              cale3=data_perfo[6],
                              bague3=data_perfo[7],
                              cale4=data_perfo[8],
                              bague4=data_perfo[9],
                              cale5=data_perfo[10],
                              bague5=data_perfo[11],
                              cale6=data_perfo[12],
                              bague6=data_perfo[13],
                              cale7=data_perfo[14],
                              bague7=data_perfo[15])
            perfo_store.add_perfo(new_perfo)

    def read_xls(self):
        self.get_cliche_from_xls()
        self.get_bobine_fille_from_xls()
        self.get_vente_annuelle_from_xls()

    def get_cliche_from_xls(self):
        xls = open_xls('ARTICLE CLICHE.xls')
        sheet = xls.sheet_by_name("Sage")
        max_row = sheet.nrows
        current_row = 0
        while current_row < max_row:
            self.extract_cliche_from_line(sheet, current_row)
            current_row += 1

    def get_bobine_fille_from_xls(self):
        xls = open_xls('ARTICLE BOBINE FILLE.xls')
        sheet = xls.sheet_by_name("Sage")
        max_row = sheet.nrows
        current_row = 0
        last_bobine_id = ""
        while current_row < max_row:
            self.extract_bobine_from_line(sheet, current_row, last_bobine_id)
            last_bobine_id = sheet.cell_value(current_row, 1)
            current_row += 1

    def get_vente_annuelle_from_xls(self):
        xls = open_xls('VENTE BOBINE.xls')
        sheet = xls.sheet_by_name("Sage")
        max_row = sheet.nrows
        current_row = 0
        while current_row < max_row:
            self.extract_vente_from_line(sheet, current_row)
            current_row += 1

    def extract_vente_from_line(self, sheet, current_row):
        current_id = sheet.cell_value(current_row, 0)
        current_vente_annuelle = sheet.cell_value(current_row, 7)
        if current_id[0] == "B":
            bobine = self.get_bobine_from_id(current_id)
            if isinstance(current_vente_annuelle, float) and bobine:
                bobine.set_vente_annuelle(current_vente_annuelle)

    @staticmethod
    def get_bobine_from_id(code):
        for bobine in bobine_fille_store.bobines:
            if bobine.code == code:
                return bobine
        return False

    @staticmethod
    def extract_cliche_from_line(sheet, current_row):
        current_id = sheet.cell_value(current_row, 0)
        current_name = sheet.cell_value(current_row, 1)
        current_poses = []
        if sheet.cell_value(current_row, 2):
            current_poses.append(int(sheet.cell_value(current_row, 2)))
        else:
            return
        if sheet.cell_value(current_row, 3):
            current_poses.append(int(sheet.cell_value(current_row, 3)))
        if sheet.cell_value(current_row, 4):
            current_poses.append(int(sheet.cell_value(current_row, 4)))
        if sheet.cell_value(current_row, 5):
            current_poses.append(int(sheet.cell_value(current_row, 5)))
        current_colors = []
        if sheet.cell_value(current_row, 6):
            current_colors.append(sheet.cell_value(current_row, 6))
        if sheet.cell_value(current_row, 7):
            current_colors.append(sheet.cell_value(current_row, 7))
        if sheet.cell_value(current_row, 8):
            current_colors.append(sheet.cell_value(current_row, 8))
        current_sommeil = sheet.cell_value(current_row, 9)
        current_cliche = Cliche(code=current_id,
                                name=current_name,
                                poses=current_poses,
                                colors=current_colors,
                                sommeil=current_sommeil)
        cliche_store.add_cliche(current_cliche)

    @staticmethod
    def extract_bobine_from_line(sheet, current_row, last_bobine_id):
        current_id = sheet.cell_value(current_row, 1)
        current_laize = sheet.cell_value(current_row, 3)
        if current_id == last_bobine_id or current_laize == "":
            return
        else:
            current_name = sheet.cell_value(current_row, 2)
            current_lenght = sheet.cell_value(current_row, 4) if sheet.cell_value(current_row, 4) != "" else 0
            current_color = sheet.cell_value(current_row, 5).title()
            current_gr = sheet.cell_value(current_row, 6) if sheet.cell_value(current_row, 6) != "" else 0
            current_code_cliche = []
            if sheet.cell_value(current_row, 7):
                current_code_cliche.append(sheet.cell_value(current_row, 7))
            if sheet.cell_value(current_row, 8):
                current_code_cliche.append(sheet.cell_value(current_row, 8))
            current_stock = sheet.cell_value(current_row, 9)
            current_stock_therme = sheet.cell_value(current_row, 10)
            current_creation_time = sheet.cell_value(current_row, 11)
            current_sommeil = sheet.cell_value(current_row, 12)
            current_bobine = BobineFille(code=current_id,
                                         name=current_name,
                                         color=current_color,
                                         laize=current_laize,
                                         gr=current_gr,
                                         lenght=current_lenght,
                                         codes_cliche=current_code_cliche,
                                         stock=current_stock,
                                         stock_therme=current_stock_therme,
                                         creation_time=current_creation_time,
                                         sommeil=current_sommeil)
            current_bobine.update_bobine_from_cliche()
            bobine_fille_store.add_bobine(current_bobine)

    def read_xlsm(self):
        xls = open_xls('Etude stock bobine V5 MASTER 18-02-23.xlsm')
        for sheet in xls.sheets():
            if sheet.name == "TYPE BOBINE MERE":
                start_ligne = 1
                current_ligne = start_ligne
                while current_ligne < sheet.nrows:
                    if sheet.cell_value(current_ligne, 1) == "":
                        break
                    else:
                        code = sheet.cell_value(current_ligne, 3)
                        color = str(sheet.cell_value(current_ligne, 1)).title()
                        gr = self.get_gr_bobine_mere(gr=sheet.cell_value(current_ligne, 5),
                                                     color=sheet.cell_value(current_ligne, 1))
                        bobine_mere = BobineMere(code=code,
                                                 color=color,
                                                 laize=sheet.cell_value(current_ligne, 0),
                                                 gr=gr,
                                                 lenght=sheet.cell_value(current_ligne, 6))
                        if color == "Poly":
                            bobine_poly_store.add_bobine(bobine_mere)
                        else:
                            bobine_papier_store.add_bobine(bobine_mere)
                    current_ligne += 1

    @staticmethod
    def get_gr_bobine_mere(gr, color):
        if gr != "" and color != "POLY":
            return gr
        elif color == "POLY":
            return "20µ"

    @staticmethod
    def is_sommeil(sommeil):
        if sommeil == "Sommeil":
            return True
        else:
            return False


app = Application()
