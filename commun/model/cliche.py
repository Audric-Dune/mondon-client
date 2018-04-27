# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Cliche:

    def __init__(self,
                 code=0,
                 name="",
                 poses=None,
                 colors=None,
                 sommeil=False):
        self.name = name
        self.code = code
        self.poses = poses
        self.colors = colors
        self.sommeil = sommeil

    def __str__(self):
        return "{} - {} - {} {} {})".format(self.code, self.name, self.colors, self.poses, self.sommeil)
