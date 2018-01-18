# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.constants.colors import color_blanc,\
    color_rouge,\
    color_orange,\
    color_vert,\
    color_bleu,\
    color_bleu_gris
from commun.constants.param import PERCENT_PROD_THEROIQUE_MAXI
from commun.ui.public.mondon_widget import MondonWidget
from commun.utils.drawing import draw_rectangle, draw_text


class Bar(MondonWidget):
    def __init__(self, parent, percent=0, mode="ui", display_max_value=True, parametric_color=True):
        super(Bar, self).__init__(parent=parent)
        self.set_border(color=color_bleu_gris, size=1)
        self.percent = percent
        self.mode = mode
        self.display_max_value = display_max_value
        self.parametric_color = parametric_color

    def set_percent(self, percent):
        """
        Met à jour le poucentage de la bar
        :param percent: Le nouveau pourcentage
        """
        self.percent = percent
        if percent > 100:
            self.percent = 100
        self.update()

    def get_scale(self):
        """
        Calcul le scale pour adapter la width de la bar par rapport à la width du widget
        :return: Le scale calculé
        """
        scale = self.width() / 100
        return scale

    def draw_bar_fond(self, p):
        """
        Draw le fond de la bar
        :param p: Paramètre de dessin
        """
        height = self.height()
        draw_rectangle(p, 1, 1, self.width()-2, height-2, color_blanc)

    def draw_bar(self, p):
        """
        Dessine la bar
        :param p: Paramètre de dessin
        """
        height = self.height()
        scale = self.get_scale()
        if self.percent != 0:
            if self.parametric_color:
                if self.percent < 25:
                    color = color_rouge
                elif self.percent < 50:
                    color = color_orange
                else:
                    color = color_vert
            else:
                color = color_bleu
            draw_rectangle(p, 1, 1, self.percent*scale-2, height-2, color)

    def draw_max_info(self, p):
        """
        Dessine l'information maximum théorique
        :param p: Paramètre de dessin
        """
        scale = self.get_scale()
        width = (100 - PERCENT_PROD_THEROIQUE_MAXI) * scale
        y = 0
        height = self.height()
        align = "C"
        text = "82% \n (Max.)"
        font_size = 8
        x = PERCENT_PROD_THEROIQUE_MAXI*scale
        draw_rectangle(p, PERCENT_PROD_THEROIQUE_MAXI * scale, 0 + 1, 2, self.height() - 2, color_bleu)
        draw_text(p,
                  x=x,
                  y=y,
                  width=width,
                  height=height,
                  color=color_bleu,
                  align=align,
                  font_size=font_size,
                  text=text,
                  bold=True)

    def draw_percent(self, p):
        """
        Dessine le label indiquant le pourcentage
        Si le % est inférieur à 22 on le dessine à droite la de la bar % sinon à gauche
        :param p: Paramètre de dessin
        """
        height = self.height()
        scale = self.get_scale()
        width = 150
        margin_text = 5
        if self.percent > 22:
            color_text = color_blanc
            pos_text_x = self.percent*scale-width - margin_text
            align = "D"
        else:
            color_text = color_bleu_gris
            pos_text_x = self.percent*scale + margin_text
            align = "G"
        draw_text(p,
                  x=pos_text_x,
                  y=0,
                  width=width,
                  height=height,
                  color=color_text,
                  align=align,
                  font_size=12,
                  text='{result}%'.format(result=round(self.percent, 1)))

    def draw(self, p):
        """
        Dessine la bar
        :param p: Paramètre de dessin
        """
        if self.mode != "ui":
            self._draw_border(p)
        self.draw_bar_fond(p)
        self.draw_bar(p)
        # Si le % de la bar est supérieur à la valeur maxi théorique on ne dessine pas l'indicateur valeur maxi
        if self.percent < PERCENT_PROD_THEROIQUE_MAXI and self.display_max_value:
            self.draw_max_info(p)
        self.draw_percent(p)
