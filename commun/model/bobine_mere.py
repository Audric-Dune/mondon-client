# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineMere:

    def __init__(self, code=0, laize=0, length=0, color="", gr="0g", stock=0, stock_therme=0):
        self.code = code
        self.laize = int(laize)
        self.length = int(length)
        self.color = color.capitalize()
        self.gr = gr
        self.init_stock = int(stock)
        self.init_stock_therme = int(stock_therme)
        self.stock_at_time = int(stock)
        self.stock_therme_at_time = int(stock_therme)
        self.stock_at_day_ago = int(stock)
        self.stock_therme_at_day_ago = int(stock_therme)

    def get_value(self, value_name):
        if value_name == "code":
            return self.code
        if value_name == "laize":
            return self.laize
        if value_name == "length":
            return self.length
        if value_name == "color":
            return self.color
        if value_name == "gr":
            return self.gr
        if value_name == "stock":
            return self.stock_at_time
        if value_name == "stock_therme":
            return self.stock_therme_at_time
        return 0

    def get_stock_at_time(self, day_ago=None, time=None):
        def count_bobine_mere_in_plan_prod(p_plan_prod):
            tours = p_plan_prod.tours
            length_tour = p_plan_prod.bobines_filles_selected[0].length
            length_bobine_mere = self.length
            bobine_mere = (tours * length_tour) / length_bobine_mere
            return bobine_mere
        if day_ago is None and not time:
            return
        from gestion.stores.plan_prod_store import plan_prod_store
        stock = self.init_stock
        stock_therme = self.init_stock_therme
        from commun.utils.timestamp import timestamp_at_day_ago
        ts = time if time else timestamp_at_day_ago(day_ago)
        for plan_prod in plan_prod_store.plans_prods:
            code_bobine_mere_plan_prod =\
                plan_prod.bobine_papier_selected.code if self.color != "Polypro" else plan_prod.bobine_poly_selected.code
            if timestamp_at_day_ago(0) <= plan_prod.start < ts and code_bobine_mere_plan_prod == self.code:
                stock -= count_bobine_mere_in_plan_prod(plan_prod)
                stock_therme -= count_bobine_mere_in_plan_prod(plan_prod)
        if day_ago is not None:
            self.stock_at_day_ago = round(stock, 1)
            self.stock_therme_at_day_ago = round(stock_therme, 1)
        else:
            self.stock_at_time = round(stock, 1)
            self.stock_therme_at_time = round(stock_therme, 1)

    def __str__(self):
        return "REF {}({}, {}, {}m, {}, stock {}, stock à therme {})".format(self.code,
                                                                             self.color,
                                                                             self.laize,
                                                                             self.length,
                                                                             self.gr,
                                                                             self.stock_at_time,
                                                                             self.stock_therme_at_time)
