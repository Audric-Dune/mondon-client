# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.ui.public.mondon_widget import MondonWidget


class Perfo(MondonWidget):

    def __init__(self,
                 parent=None,
                 code=0,
                 dec_init=0,
                 cale1=0,
                 bague1=0,
                 cale2=0,
                 bague2=0,
                 cale3=0,
                 bague3=0,
                 cale4=0,
                 bague4=0,
                 cale5=0,
                 bague5=0,
                 cale6=0,
                 bague6=0,
                 cale7=0,
                 bague7=0):
        super(Perfo, self).__init__(parent=parent)
        self.code = code,
        self.dec_init = dec_init,
        self.cale1 = cale1,
        self.bague1 = bague1,
        self.cale2 = cale2,
        self.bague2 = bague2,
        self.cale3 = cale3,
        self.bague3 = bague3,
        self.cale4 = cale4,
        self.bague4 = bague4,
        self.cale5 = cale5,
        self.bague5 = bague5,
        self.cale6 = cale6,
        self.bague6 = bague6,
        self.cale7 = cale7,
        self.bague7 = bague7

    def __str__(self):
        return "PERFO{} : {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(self.id,
                                                                                             self.dec_init,
                                                                                             self.cale1,
                                                                                             self.bague1,
                                                                                             self.cale2,
                                                                                             self.bague2,
                                                                                             self.cale3,
                                                                                             self.bague3,
                                                                                             self.cale4,
                                                                                             self.bague4,
                                                                                             self.cale5,
                                                                                             self.bague5,
                                                                                             self.cale6,
                                                                                             self.bague6,
                                                                                             self.cale7,
                                                                                             self.bague7)
