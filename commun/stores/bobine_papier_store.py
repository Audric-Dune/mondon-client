# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobinePapierStore:
    def __init__(self):
        self.bobines = []

    def add_bobine(self, bobine):
        self.bobines.append(bobine)


bobine_papier_store = BobinePapierStore()
