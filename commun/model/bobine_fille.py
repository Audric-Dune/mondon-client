# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BobineFille:

    def __init__(self,
                 code=0,
                 name="",
                 laize=0.,
                 length=0,
                 color="",
                 stock=0,
                 stock_therme=0,
                 creation_time=0,
                 codes_cliche=None,
                 colors_cliche=None,
                 gr=0,
                 poses=None,
                 sommeil=False):
        self.name = name
        self.code = code
        self.codes_cliche = codes_cliche
        self.colors_cliche = colors_cliche
        self.laize = float(laize)
        self.length = int(length)
        self.color = color
        self.init_stock = stock
        self.stock_at_day_ago = stock
        self.stock_at_time = stock
        self.init_stock_therme = stock_therme
        self.stock_therme_at_day_ago = stock_therme
        self.stock_therme_at_time = stock_therme
        self.creation_time = creation_time
        self.gr = gr
        self.poses = poses if poses else [0]
        self.init_sommeil = sommeil
        self.sommeil = "Sommeil" if sommeil else ""
        self.vente_annuelle = 0
        self.vente_mensuelle = 0
        self.etat = ""
        self.qte_a_prod = 0
        self.contrainte = [self.color, self.gr, self.length]
        self.update_bobine_from_cliche()

    def get_new_bobine_with_poses(self, poses):
        return BobineFille(code=self.code,
                           name=self.name,
                           laize=self.laize,
                           length=self.length,
                           color=self.color,
                           stock=self.init_stock,
                           stock_therme=self.init_stock_therme,
                           creation_time=self.creation_time,
                           codes_cliche=self.codes_cliche,
                           colors_cliche=self.colors_cliche,
                           gr=self.gr,
                           poses=poses,
                           sommeil=self.init_sommeil)

    def update_bobine_from_cliche(self):
        """
        Met à jour la bobine (poses et couleur de poses) en fonction des codes clichés
        """
        # Test si on a des clichés associés à la bobine
        if self.codes_cliche:
            # Parcour les clichés associés à la bobine
            for code_cliche in self.codes_cliche:
                # Récupère les poses et couleurs associés au cliché
                poses_and_colors = self.get_poses_and_colors_from_code_cliche(code_cliche)
                if poses_and_colors:
                    poses_cliche = poses_and_colors[0].copy()
                    colors_cliche = poses_and_colors[1].copy()
                    # Si la bobine ne contient pas encore de poses (self.poses = [0])
                    # on initialise les poses et couleurs avec le cliché courant
                    if self.poses[0] == 0:
                        self.poses = poses_cliche
                        self.colors_cliche = colors_cliche
                    # Si la bobine contient des poses
                    else:
                        # On ajoute les nouvelles couleurs
                        for color_cliche in colors_cliche:
                            if color_cliche in self.colors_cliche:
                                continue
                            else:
                                self.colors_cliche.append(color_cliche)
                        # On vérifie que les poses sont compatible avec les nouvelles poses cliché
                        for pose in self.poses:
                            if pose in poses_cliche:
                                continue
                            # On retire la pose si incompatible avec la nouvelles pose cliché
                            try:
                                poses_cliche.remove(pose)
                            except ValueError:
                                pass

    def set_vente_annuelle(self, current_vente_annuelle):
        self.vente_annuelle = current_vente_annuelle
        self.vente_mensuelle = round(current_vente_annuelle/12, 1)
        self.get_etat()

    def get_etat(self):
        from commun.utils.seuil_alerte import get_etat, get_qte_a_prod
        self.etat = get_etat(bobine=self)
        self.qte_a_prod = int(get_qte_a_prod(bobine=self))

    def get_stock_at_time(self, day_ago=None, time=None):
        def get_piste_in_plan_prod(p_bobine, p_plan_prod):
            piste = 0
            for p_bobine_in_plan_prod in p_plan_prod.bobines_filles_selected:
                if p_bobine.code == p_bobine_in_plan_prod.code:
                    piste += 1 if p_bobine_in_plan_prod.pose == 0 else p_bobine_in_plan_prod.pose
            return piste if piste > 0 else None
        if day_ago is None and not time:
            return
        from gestion.stores.plan_prod_store import plan_prod_store
        stock = self.init_stock
        stock_therme = self.init_stock_therme
        from commun.utils.timestamp import timestamp_at_day_ago
        ts = time if time else timestamp_at_day_ago(day_ago)
        for plan_prod in plan_prod_store.plans_prods:
            if timestamp_at_day_ago(0) <= plan_prod.start < ts:
                piste_in_plan_prod = get_piste_in_plan_prod(self, plan_prod)
                if piste_in_plan_prod:
                    stock += piste_in_plan_prod * plan_prod.tours
                    stock_therme += piste_in_plan_prod * plan_prod.tours
        if day_ago is not None:
            self.stock_at_day_ago = stock
            self.stock_therme_at_day_ago = stock_therme
        else:
            self.stock_at_time = stock
            self.stock_therme_at_time = stock_therme
        self.get_etat()

    @staticmethod
    def get_poses_and_colors_from_code_cliche(code_cliche):
        from commun.stores.cliche_store import cliche_store
        for cliche in cliche_store.cliches:
            if cliche.code == code_cliche:
                return cliche.poses, cliche.colors

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
        if value_name == "stock_at_time":
            return self.stock_at_time
        if value_name == "stock_therme_at_time":
            return self.stock_therme_at_time
        if value_name == "vente_annuelle":
            return self.vente_annuelle
        if value_name == "vente_mensuelle":
            return self.vente_mensuelle
        if value_name == "qte_a_prod":
            return self.qte_a_prod
        return 0

    def __repr__(self):
        return '{}, {}, {}, {}, {}, {}'.format(self.code, self.laize, self.poses, self.color, self.gr, self.length)
