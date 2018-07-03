# !/usr/bin/env python
# -*- coding: utf-8 -*-


def group_bobine(bobines):
    dict_bobines = {}
    bobines = sorted(bobines, key=lambda b: b.get_value("code"), reverse=False)
    for bobine in bobines:
        pose = bobine.pose if bobine.pose else 1
        if dict_bobines.get(bobine.code):
            dict_bobines[bobine.code][1] += pose
        else:
            dict_bobines[bobine.code] = []
            dict_bobines[bobine.code].append(bobine)
            dict_bobines[bobine.code].append(pose)
    return dict_bobines
