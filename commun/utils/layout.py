# !/usr/bin/env python
# -*- coding: utf-8 -*-


def clear_layout(layout):
    """
    Supprime tous les enfant d'un layout
    :param layout: Le layout a clear
    :return:
    """
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clear_layout(item.layout())
    return layout
