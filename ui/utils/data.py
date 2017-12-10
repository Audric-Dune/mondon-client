# !/usr/bin/env python
# -*- coding: utf-8 -*-


def affiche_entier(s, sep=' '):
    s = str(s)
    if len(s) <= 3:
        return s
    else:
        return affiche_entier(s[:-3]) + sep + s[-3:]
