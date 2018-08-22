# !/usr/bin/env python
# -*- coding: utf-8 -*-


class DataReglage:

    def __init__(self, reglage):
        self.reglage = reglage
        self.check_box_conducteur = False
        self.check_box_aide = False

    def flip_check_box(self, name_check_box):
        if name_check_box == "conducteur":
            self.check_box_conducteur = False if self.check_box_conducteur else True
        if name_check_box == "aide":
            self.check_box_aide = False if self.check_box_aide else True
