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
        self.stock = stock
        self.stock_therme = stock_therme
        self.creation_time = creation_time
        self.gr = gr
        self.poses = poses if poses else [0]
        self.sommeil = "Sommeil" if sommeil else ""
        self.vente_annuelle = 0
        self.vente_mensuelle = 0
        self.etat = ""

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
                    poses_cliche = poses_and_colors[0]
                    colors_cliche = poses_and_colors[1]
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
                            else:
                                poses_cliche.remove(pose)

    def set_vente_annuelle(self, current_vente_annuelle):
        self.vente_annuelle = current_vente_annuelle
        self.vente_mensuelle = round(current_vente_annuelle/12, 1)
        self.get_etat()

    def get_etat(self):
        if self.vente_mensuelle > self.stock_therme:
            self.etat = "RUPTURE"
        elif self.vente_annuelle < self.stock_therme:
            self.etat = "SURSTOCK"

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
        if value_name == "stock":
            return self.stock
        if value_name == "stock_therme":
            return self.stock_therme
        if value_name == "vente_mensuelle":
            return self.vente_mensuelle
        return 0

    def __repr__(self):
        return "B{} ({}, {}, {}m, {} poses, {}, {}), {}g, {}".format(self.code,
                                                                     self.color,
                                                                     self.laize,
                                                                     self.length,
                                                                     self.poses,
                                                                     self.codes_cliche,
                                                                     self.colors_cliche,
                                                                     self.gr,
                                                                     self.sommeil)
