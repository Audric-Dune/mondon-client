# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineFilleStore:
    def __init__(self):
        self.bobines = []

    def add_bobine(self, bobine):
        self.bobines.append(bobine)

    def sort_bobines(self, sort_name, sort_asc):
        self.bobines = sorted(self.bobines, key=lambda b: b.get_value(sort_name), reverse= not sort_asc)


bobine_fille_store = BobineFilleStore()
