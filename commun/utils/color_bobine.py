# !/usr/bin/env python
# -*- coding: utf-8 -*-
from commun.constants.colors import \
    bob_blanc,\
    bob_ecru,\
    bob_ivoire,\
    bob_jaune,\
    bob_marron,\
    bob_noir,\
    bob_orange,\
    bob_prune,\
    bob_rouge,\
    bob_vert,\
    color_bleu_gris


def get_color_bobine(bobine_color):
    color = color_bleu_gris
    if bobine_color == "Blanc":
        color = bob_blanc
    if bobine_color == "Noir":
        color = bob_noir
    if bobine_color == "Rouge":
        color = bob_rouge
    if bobine_color == "Vert":
        color = bob_vert
    if bobine_color == "Marron":
        color = bob_marron
    if bobine_color == "Orange":
        color = bob_orange
    if bobine_color == "Prune":
        color = bob_prune
    if bobine_color == "Ecru" or bobine_color == "Ecru Enduit":
        color = bob_ecru
    if bobine_color == "Jaune":
        color = bob_jaune
    if bobine_color == "Ivoire":
        color = bob_ivoire
    return color
