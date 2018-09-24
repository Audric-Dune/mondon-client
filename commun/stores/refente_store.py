# !/usr/bin/env python
# -*- coding: utf-8 -*-


class RefenteStore:
    def __init__(self):
        self.refentes = []

    def add_item(self, refente):
        self.refentes.append(refente)


refente_store = RefenteStore()
