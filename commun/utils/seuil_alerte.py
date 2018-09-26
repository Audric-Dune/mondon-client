# !/usr/bin/env python
# -*- coding: utf-8 -*-

seuil_alerte = []


def get_etat(bobine):
    for seuil in seuil_alerte:
        if seuil['p_min'] <= bobine.vente_annuelle <= seuil['p_max']:
            if bobine.stock_therme_at_time < seuil['p_seuil']:
                return "RUPTURE"
            if bobine.vente_annuelle < bobine.stock_therme_at_time:
                return "SURSTOCK"
            else:
                return ""


def get_qte_a_prod(bobine):
    for seuil in seuil_alerte:
        if seuil['p_min'] <= bobine.vente_annuelle <= seuil['p_max']:
            if bobine.vente_annuelle < bobine.stock_therme_at_time:
                return 0
            else:
                return seuil['p_qte']
    return 0
