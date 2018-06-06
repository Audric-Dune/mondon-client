# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineFilleValid:
    def __init__(self, bobine, valid_poses):
        self.bobine = bobine
        self.valid_poses = valid_poses

    def __getattr__(self, attr):
        if attr == "valid_poses":
            return self.valid_poses
        else:
            return getattr(self.bobine, attr)
