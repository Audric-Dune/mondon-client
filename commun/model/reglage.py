# !/usr/bin/env python
# -*- coding: utf-8 -*-


from commun.utils.cliches import get_cliche_from_code


class Reglage:

    def __init__(self, p_id=None, cat=None, des=None, time=None, optionnel=False, info=None):
        self.id = int(p_id)
        self.cat = cat
        self.des = des
        self.time = int(time)
        self.optionnel = optionnel
        self.info = info
        self.qty = 1

    def is_active(self, p, last_p):
        """
        Détermine si la ligne est active en fonction du plan de production et de l'ancien plan de production
        Met à jour le paramètre qty (correspond au nombre de fois que doit être exécuté le réglage) si besoin
        :param p: plan de production
        :param last_p: ancien plan de prod
        :return: True si le réglage est actif
        """
        if last_p is None:
            return False
        if self.id == 0 or self.id == 23:
            if p.perfo_selected and p.perfo_selected.code == last_p.perfo_selected.code:
                return False
            return True
        if self.id == 1 or self.id == 2 or self.id == 3 or self.id == 20 or self.id == 21:
            if p.refente_selected and p.refente_selected.code == last_p.refente_selected.code:
                return False
            return True
        if self.id == 4:
            if p.bobine_papier_selected is None:
                return True
            if p.bobine_papier_selected.code == last_p.bobine_papier_selected.code:
                return False
            return True
        p_cliche = self.get_cliche_from_plan_prod(plan_prod=p)
        last_p_cliche = self.get_cliche_from_plan_prod(plan_prod=last_p)
        if self.id == 12:
            for tuple_cliche in p_cliche:
                if tuple_cliche in last_p_cliche:
                    last_p_cliche.remove(tuple_cliche)
            qty = 0
            for tuple_cliche in last_p_cliche:
                cliche = get_cliche_from_code(tuple_cliche[0])
                qty += len(cliche.colors) if cliche else 0
                return False
            self.qty = qty
            return True
        if self.id == 14 or self.id == 15:
            for tuple_cliche in p_cliche:
                if tuple_cliche in last_p_cliche:
                    p_cliche.remove(tuple_cliche)
            qty = 0
            for tuple_cliche in p_cliche:
                cliche = get_cliche_from_code(tuple_cliche[0])
                if cliche:
                    qty += len(cliche.colors)
            if qty == 0:
                return False
            self.qty = qty
            return True
        if self.id == 16:
            qty = 0
            for i in range(1, 4):
                if self.color_encrier_changed(encrier=getattr(p, "encrier_{}".format(i)),
                                              last_encrier=getattr(last_p, "encrier_{}".format(i))):
                    qty += 1
            if qty == 0:
                return False
            self.qty = qty
            return True
        if self.id == 17:
            qty = 0
            for i in range(1, 4):
                if self.remplissage_encrier(encrier=getattr(p, "encrier_{}".format(i)),
                                            last_encrier=getattr(last_p, "encrier_{}".format(i))):
                    qty += 1
            if qty == 0:
                return False
            self.qty = qty
            return True
        if self.id == 18:
            qty = 0
            for tuple_cliche in p_cliche:
                cliche = get_cliche_from_code(tuple_cliche[0])
                qty_color = len(cliche.colors)
                if qty_color == 1:
                    continue
                if qty_color == 2:
                    qty = 1
                if qty_color == 2:
                    self.qty = 2
                    return True
            if qty == 0:
                return False
            self.qty = qty
            return True
        if self.id == 22:
            qty_laize_from_p = self.get_qty_laize_from_plan_prod(plan_prod=p)
            qty_laize_from_last_p = self.get_qty_laize_from_plan_prod(plan_prod=last_p)
            if qty_laize_from_p > qty_laize_from_last_p:
                return True
        if self.id == 24:
            if p.bobine_poly_selected is None:
                return True
            if p.bobine_poly_selected.code == last_p.bobine_poly_selected.code:
                return False
            return True

    @staticmethod
    def get_cliche_from_plan_prod(plan_prod):
        cliches = []
        b_selected = plan_prod.bobines_filles_selected
        for b in b_selected:
            if b.codes_cliche:
                pose = b.pose
                for code_cliche in b.codes_cliche:
                    cliches.append((code_cliche, pose))
        return cliches

    @staticmethod
    def color_encrier_changed(encrier, last_encrier):
        if encrier.color is None or last_encrier.color is None:
            return False
        if encrier.color[:1] == "_":
            return False
        if encrier.color == last_encrier.color:
            return False
        return True

    def remplissage_encrier(self, encrier, last_encrier):
        if self.color_encrier_changed(encrier, last_encrier):
            return True
        if last_encrier.color is None and encrier.color is not None and encrier.color[:1] != "_":
            return True

    @staticmethod
    def get_qty_laize_from_plan_prod(plan_prod):
        qty = 0
        if plan_prod.refente_selected:
            laizes = plan_prod.refente_selected.laizes
            for laize in laizes:
                if laize:
                    qty += 1
        return qty

    def is_optionnel(self):
        if self.optionnel:
            return True
        return False

    def __str__(self):
        return "ID {}, {}: {} temps: {}min (optionnel: {})".format(self.id,
                                                                   self.cat,
                                                                   self.des,
                                                                   self.time,
                                                                   self.is_optionnel())
