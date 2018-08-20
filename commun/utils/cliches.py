# !/usr/bin/env python
# -*- coding: utf-8 -*-


def get_cliche_from_code(code_cliche):
    from commun.stores.cliche_store import cliche_store
    for cliche in cliche_store.cliches:
        if cliche.code == code_cliche:
            return cliche
