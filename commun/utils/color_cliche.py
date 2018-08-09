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
    color = color_bleu_gris
    if color_cliche == "Blanc":
        color = cliche_blanc
    if color_cliche == "Noir":
        color = cliche_noir
    if color_cliche == "Rouge":
        color = cliche_rouge
    if color_cliche == "Vert":
        color = cliche_vert
    if color_cliche == "Bistre":
        color = cliche_bistre
    if color_cliche == "Orange":
        color = cliche_orange
    if color_cliche == "Jaune":
        color = cliche_jaune
    if color_cliche == "Bleu":
        color = cliche_bleu
    return color
