# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineFilleSelected:
    def __init__(self, bobine, pose, index=None):
        self.bobine = bobine
        self.index = index
        self.pose = pose

    def __getattr__(self, attr):
        if attr == "index":
            return self.index
        elif attr == "pose":
            return self.pose
        else:
            return getattr(self.bobine, attr)

    def __repr__(self):
        return '{}, pose {}, index {}'.format(self.code,
                                              self.pose,
                                              self.index)

    def __lt__(self, other):
        return self.pose < other.pose if self.code == other.code else self.code < other.code

    def __hash__(self):
        h = hash('{}({})'.format(self.code, self.pose))
        return h
