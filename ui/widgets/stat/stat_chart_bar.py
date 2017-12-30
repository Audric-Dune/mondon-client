# !/usr/bin/env python
# -*- coding: utf-8 -*-

from constants.colors import color_bleu_gris, color_blanc, color_noir
from ui.widgets.public.mondon_widget import MondonWidget
from ui.utils.drawing import draw_text, draw_rectangle
from ui.utils.data import affiche_entier


class StatChartBar(MondonWidget):
    """
    S'occupe de dessiner une bar avec ca valeur
    """
    PADDING_MAX_VALUE = 30
    PADDING_LABEL_H = 2
    PADDING_LABEL_V = 5

    def __init__(self, value, color, max_value, parent=None):
        super(StatChartBar, self).__init__(parent=parent)
        self.text_value = str(affiche_entier(value))
        self.value = value
        self.max_value = max_value
        self.color_label = color_blanc
        self.color_bar = color
        if value < 0:
            self.text_value = "NA"
        self.height_bar = 0
        self.set_background_color(color_blanc)

    def draw_label(self, p):
        """
        Dessine la valeur de la bar
        :param p: Paramètre de dessin
        """
        # Si la largeur est suffisante on trace la valeur horizontalement
        if self.width() > 80:
            draw_text(p, 0, self.height()-self.height_bar-20-self.PADDING_LABEL_H, self.width(), 20,
                      color=color_bleu_gris, align="C", font_size=12, text=self.text_value)
        else:
            # Sinon on trace la valeur verticalement
            p.rotate(90)
            # Si la hauteur est suffisante on trace la valeur à l'intérieur de la bar
            if self.height_bar > 50:
                draw_text(p, self.height()-self.height_bar+self.PADDING_LABEL_V, -self.width() / 2 - 10.5, 200, 20,
                          color=color_blanc, align="G", font_size=12, text=self.text_value)
            # Sinon la valeur à l'extérieur de la bar
            else:
                draw_text(p, self.height()-self.height_bar-200-self.PADDING_LABEL_V, -self.width() / 2 - 10.5, 200, 20,
                          color=color_noir, align="D", font_size=12, text=self.text_value)

    def draw_bar(self, p):
        """
        Dessine la bar
        :param p: Parmaètre de dessin
        """
        draw_rectangle(p, 0, self.height()-self.height_bar, self.width(), self.height_bar, self.color_bar)

    def get_height_bar(self):
        """
        Calcul la hauteur de la bar par rapport à la valeur maximum de la série
        """
        if self.max_value and self.value >= 0:
            self.height_bar = self.value * (self.height() - self.PADDING_MAX_VALUE) / self.max_value
        else:
            self.height_bar = 0
        self.height_bar = round(self.height_bar)

    def draw(self, p):
        """
        Fonction appelé automatiquement, s'occupe de récupérer la hauteur de la bar et de dessiner la bar et sa valeur
        :param p: Paramètre de dessin
        """
        self.get_height_bar()
        self._draw_fond(p)
        self.draw_bar(p)
        self.draw_label(p)
