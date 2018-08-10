# !/usr/bin/env python
# -*- coding: utf-8 -*-
from commun.constants.colors import \
    cliche_bistre,\
    cliche_blanc, \
    cliche_bleu, \
    cliche_jaune, \
    cliche_noir, \
    cliche_orange, \
    cliche_rouge, \
    cliche_vert,\
    color_bleu_gris


def get_color_cliche(color_cliche):
    p_color_cliche = color_cliche.capitalize()
    color = color_bleu_gris
    if p_color_cliche == "Blanc":
        color = cliche_blanc
    if p_color_cliche == "Noir":
        color = cliche_noir
    if p_color_cliche == "Rouge":
        color = cliche_rouge
    if p_color_cliche == "Vert":
        color = cliche_vert
    if p_color_cliche == "Bistre":
        color = cliche_bistre
    if p_color_cliche == "Orange":
        color = cliche_orange
    if p_color_cliche == "Jaune":
        color = cliche_jaune
    if p_color_cliche == "Bleu":
        color = cliche_bleu
    return color
