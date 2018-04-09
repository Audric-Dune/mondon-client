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
    print(bobine_color)
    color = color_bleu_gris
    if bobine_color == "BLANC":
        color = bob_blanc
    if bobine_color == "NOIR":
        color = bob_noir
    if bobine_color == "ROUGE":
        color = bob_rouge
    if bobine_color == "VERT":
        color = bob_vert
    if bobine_color == "MARRON":
        color = bob_marron
    if bobine_color == "ORANGE":
        color = bob_orange
    if bobine_color == "PRUNE":
        color = bob_prune
    if bobine_color == "ECRU":
        color = bob_ecru
    if bobine_color == "JAUNE":
        color = bob_jaune
    if bobine_color == "IVOIRE":
        color = bob_ivoire
    return color
