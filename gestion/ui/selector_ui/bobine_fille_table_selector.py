# !/usr/bin/env python
# -*- coding: utf-8 -*-

from commun.utils.core_table import TableModel


class BobineFilleTableSelector(TableModel):

    def __init__(self, plan_prod):
        super(BobineFilleTableSelector, self).__init__()
        self.plan_prod = plan_prod

    def get_elements(self):
        """
        Définit la liste des objets à afficher dans la table
        """
        return self.plan_prod.current_bobine_fille_store.bobines
