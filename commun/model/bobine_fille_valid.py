# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineFilleValid:
    def __init__(self, bobine):
        self.bobine = bobine
        self.valid_poses = bobine.poses

    def __getattr__(self, attr):
        if attr == "valid_poses":
            return self.valid_poses
        else:
            return getattr(self.bobine, attr)

    def __repr__(self):
        return '{}, {}, {}, {}, {}, {}'.format(self.code,
                                               self.laize,
                                               self.color,
                                               self.gr,
                                               self.length,
                                               self.poses)
