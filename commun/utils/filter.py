# !/usr/bin/env python
# -*- coding: utf-8 -*-

import copy


# FILTRE BOBINES PAPIER


def filter_bobines_papier_for_contrainte(bobines_papier, contrainte):
    new_bobines_papier = []
    for bobine_papier in bobines_papier:
        if is_valid_bobine_papier_for_contrainte(bobine_papier, contrainte):
            new_bobines_papier.append(bobine_papier)
    return new_bobines_papier


def filter_bobines_papier_for_refentes(bobines_papier, refentes):
    new_bobines_papier = []
    for bobine_papier in bobines_papier:
        if is_valid_bobine_papier_for_refentes(bobine_papier, refentes):
            new_bobines_papier.append(bobine_papier)
    return new_bobines_papier


def filter_bobines_papier_for_bobines_fille(bobines_papier, bobines_fille):
    new_bobines_papier = []
    for bobine_papier in bobines_papier:
        if is_valid_bobine_papier_for_bobines_fille(bobine_papier, bobines_fille):
            new_bobines_papier.append(bobine_papier)
    return new_bobines_papier


def is_valid_bobine_papier_for_refentes(bobine_papier, refentes):
    if not refentes:
        return True
    for refente in refentes:
        if is_valid_bobine_papier_for_refente(bobine_papier, refente):
            return True
    return False


def is_valid_bobine_papier_for_contrainte(bobine_papier, contrainte):
    if not is_valid_bobine_papier_for_bobine_poly(bobine_papier, bobine_poly=contrainte.bobine_poly):
        return False
    if not is_valid_bobine_papier_for_bobine_papier(bobine_papier, bobine_papier_contrainte=contrainte.bobine_papier):
        return False
    if not is_valid_bobine_papier_for_refente(bobine_papier, refente=contrainte.refente):
        return False
    if not is_valid_bobine_papier_for_bobines_fille(bobine_papier, bobines_fille=contrainte.bobines_fille):
        return False
    return True


def is_valid_bobine_papier_for_bobine_poly(bobine_papier, bobine_poly):
    if not bobine_poly:
        return True
    if bobine_papier.laize == bobine_poly.laize:
        return True
    return False


def is_valid_bobine_papier_for_bobine_papier(bobine_papier, bobine_papier_contrainte):
    if not bobine_papier_contrainte:
        return True
    if bobine_papier.code == bobine_papier_contrainte.code:
            return True
    return False


def is_valid_bobine_papier_for_refente(bobine_papier, refente):
    if not refente:
        return True
    if bobine_papier.laize == refente.laize:
        return True
    return False


def is_valid_bobine_papier_for_bobines_fille(bobine_papier, bobines_fille):
    if not bobines_fille:
        return True
    for bobine_fille in bobines_fille:
        if is_valid_bobine_papier_for_bobine_fille(bobine_papier, bobine_fille):
            return True
    return False


def is_valid_bobine_papier_for_bobine_fille(bobine_papier, bobine_fille):
    if not bobine_fille:
        return True
    if bobine_papier.color != bobine_fille.color:
        return False
    if bobine_papier.gr != bobine_fille.gr:
        return False
    return True


# FILTRE REFENTES


def filter_refentes_for_contrainte(refentes, contrainte):
    new_refentes = []
    for refente in refentes:
        if is_valid_refente_for_contrainte(refente, contrainte):
            new_refentes.append(refente)
    return new_refentes


def filter_refentes_for_bobines_papier(refentes, bobines_papier):
    new_refentes = []
    for refente in refentes:
        if is_valid_refente_for_bobines_papier(refente, bobines_papier):
            new_refentes.append(refente)
    return new_refentes


def filter_refentes_for_bobines_fille(refentes, bobines_fille, bobines_fille_selected):
    new_refentes = []
    for refente in refentes:
        if is_valid_refente_for_bobines_fille(refente, bobines_fille, bobines_fille_selected):
            new_refentes.append(refente)
    return new_refentes


def is_valid_refente_for_bobines_papier(refente, bobines_papier):
    if not bobines_papier:
        return True
    for bobine_papier in bobines_papier:
        if is_valid_refente_for_bobine_papier(refente, bobine_papier):
            return True
    return False


def is_valid_refente_for_contrainte(refente, contrainte):
    if not is_valid_refente_for_bobine_poly(refente, bobine_poly=contrainte.bobine_poly):
        return False
    if not is_valid_refente_for_perfo(refente, perfo=contrainte.perfo):
        return False
    if not is_valid_refente_for_bobine_papier(refente, bobine_papier=contrainte.bobine_papier):
        return False
    if not is_valid_refente_for_refente(refente, refente_contrainte=contrainte.refente):
        return False
    if not is_valid_refente_for_bobines_fille_selected(refente, bobines_fille_selected=contrainte.bobines_fille):
        return False
    return True


def is_valid_refente_for_bobine_poly(refente, bobine_poly):
    if not bobine_poly:
        return True
    if refente.laize == bobine_poly.laize:
        return True
    return False


def is_valid_refente_for_perfo(refente, perfo):
    if not perfo:
        return True
    if refente.code_perfo == perfo.code:
        return True
    return False


def is_valid_refente_for_bobine_papier(refente, bobine_papier):
    if not bobine_papier:
        return True
    if refente.laize == bobine_papier.laize:
        return True
    return False


def is_valid_refente_for_refente(refente, refente_contrainte):
    if not refente_contrainte:
        return True
    if refente.code == refente_contrainte.code:
        return True
    return False


def is_valid_refente_for_bobines_fille_selected(refente, bobines_fille_selected):
    if not bobines_fille_selected:
        return True
    new_refente = refente
    for bobine in bobines_fille_selected:
        new_refente = get_new_refente_with_bobine_fille(refente=new_refente, bobine_fille=bobine)
        if not new_refente:
            return False
    return True


def is_valid_refente_for_bobines_fille(refente, bobines_fille, bobines_fille_selected):
    refente_with_bobines_fille_selected = get_new_refente_with_bobines_fille(refente,
                                                                             bobines_fille=bobines_fille_selected)
    if is_full_refente_with_bobines_fille_selected(refente=refente_with_bobines_fille_selected):
        return True
    for bobine in bobines_fille:
        for pose in bobine.poses:
            from commun.model.bobine_fille_selected import BobineFilleSelected
            bobine_fille_selected = BobineFilleSelected(bobine=bobine, pose=pose)
            if not is_valid_bobine_fille_and_pose_for_bobines_fille(bobine_fille_selected,
                                                                    pose,
                                                                    bobines_fille=bobines_fille_selected):
                continue
            elif not is_valid_bobine_fille_and_pose_for_refente(bobine_fille=bobine_fille_selected,
                                                                refente=refente,
                                                                bobines_fille_selected=bobines_fille_selected):
                continue
            else:
                new_bobines_fille_selected = bobines_fille_selected.copy()
                new_bobines_fille_selected.append(bobine_fille_selected)
                if is_valid_refente_for_bobines_fille(refente=refente,
                                                      bobines_fille=bobines_fille,
                                                      bobines_fille_selected=new_bobines_fille_selected):
                    return True
    return False


def is_full_refente_with_bobines_fille_selected(refente):
    for laize in refente.laizes:
        if laize:
            return False
    return True


def is_valid_bobine_fille_and_pose_for_bobines_fille(bobine_to_validate, pose, bobines_fille):
    if pose == 0:
        return True
    poses = bobine_to_validate.poses.copy()
    for bobine in bobines_fille:
        if bobine_to_validate.code == bobine.code and pose == bobine.pose:
            poses.remove(pose)
            if pose in poses:
                pass
            else:
                return False
    return True


def get_new_refente_with_bobines_fille(refente, bobines_fille):
    new_refente = refente
    for bobine in bobines_fille:
        new_refente = get_new_refente_with_bobine_fille(new_refente, bobine)
    return new_refente


def get_new_refente_with_bobine_fille(refente, bobine_fille):
    start_index = 0
    counter_pose = 0
    bobine_pose = bobine_fille.pose if bobine_fille.pose != 0 else 1
    is_valid_bobine = False
    for laize_refente in refente.laizes:
        if laize_refente and laize_refente == bobine_fille.laize:
            counter_pose += 1
            if counter_pose >= bobine_pose:
                is_valid_bobine = True
                break
        else:
            counter_pose = 0
            start_index += 1
    if not is_valid_bobine:
        return False
    from commun.model.refente import Refente
    new_refente = Refente()
    index_refente = 0
    for laize_refente in refente.laizes:
        if index_refente < start_index or index_refente >= start_index + bobine_pose:
            new_refente.laizes[index_refente] = laize_refente
        index_refente += 1
    return new_refente


def is_valid_laize_for_bobines_fille(laize, bobines_fille):
    if not laize:
        return True
    for bobine in bobines_fille:
        if bobine.laize == laize:
            return True
    return False


# FILTRE BOBINES FILLE


def filter_bobines_fille_for_contrainte(bobines_fille, contrainte):
    new_bobines_fille = []
    for bobine_fille in bobines_fille:
        if is_valid_bobine_fille_for_contrainte(bobine_fille, contrainte):
            new_bobines_fille.append(bobine_fille)
    return new_bobines_fille


def filter_bobines_fille_for_bobines_papier(bobines_fille, bobines_papier):
    new_bobines_fille = []
    for bobine_fille in bobines_fille:
        if is_valid_bobine_fille_for_bobines_papier(bobine_fille, bobines_papier):
            new_bobines_fille.append(bobine_fille)
    return new_bobines_fille


def filter_bobines_fille_for_refentes(bobines_fille, refentes, bobines_fille_selected):
    new_bobines_fille = []
    for bobine_fille in bobines_fille:
        if is_valid_bobine_fille_for_refentes(bobine_fille, refentes, bobines_fille_selected):
            new_bobines_fille.append(bobine_fille)
    return new_bobines_fille


def is_valid_bobine_fille_for_refentes(bobine_fille, refentes, bobines_fille_selected):
    for refente in refentes:
        if is_valid_bobine_fille_for_refente(bobine_fille, refente, bobines_fille_selected):
            return True
    return False


def is_valid_bobine_fille_for_bobines_papier(bobine_fille, bobines_papier):
    for bobine_papier in bobines_papier:
        if is_valid_bobine_fille_for_bobine_papier(bobine_fille, bobine_papier):
            return True
    return False


def is_valid_bobine_fille_for_contrainte(bobine_fille, contrainte):
    if not is_valid_bobine_fille_for_bobine_papier(bobine_fille, bobine_papier=contrainte.bobine_papier):
        return False
    if not is_valid_bobine_fille_for_refente(bobine_fille,
                                             refente=contrainte.refente,
                                             bobines_fille_selected=contrainte.bobines_fille):
        return False
    if not is_valid_bobine_fille_for_bobines_fille(bobine_fille, bobines_fille=contrainte.bobines_fille):
        return False
    return True


def is_valid_bobine_fille_for_bobine_papier(bobine_fille, bobine_papier):
    if not bobine_papier:
        return True
    if bobine_fille.color != bobine_papier.color:
        return False
    if bobine_fille.gr != bobine_papier.gr:
        return False
    return True


def is_valid_bobine_fille_for_refente(bobine_fille, refente, bobines_fille_selected):
    if not refente:
        return True
    new_refente = get_new_refente_with_bobines_fille(refente, bobines_fille=bobines_fille_selected)
    count_pose = 0
    for laize in new_refente.laizes:
        if bobine_fille.laize == laize:
            count_pose += 1
            for pose in bobine_fille.poses:
                if pose == 0:
                    return True
                if pose == count_pose:
                    return True
    return False


def is_valid_bobine_fille_and_pose_for_refente(bobine_fille, refente, bobines_fille_selected):
    if not refente:
        return True
    new_refente = get_new_refente_with_bobines_fille(refente, bobines_fille=bobines_fille_selected)
    count_pose = 0
    for laize in new_refente.laizes:
        if bobine_fille.laize == laize:
            count_pose += 1
            if bobine_fille.pose == 0:
                return True
            if bobine_fille.pose == count_pose:
                return True
    return False


def is_valid_bobine_fille_for_bobines_fille(bobine_fille, bobines_fille):
    if not bobines_fille:
        return True
    # Bobine_fille:
    # poses = [listes des poses disponible]; exemple: [1,2,4]
    # pose = pose sélectionnée dans la list des poses; exemple: 2
    poses = bobine_fille.poses.copy()
    for bobine_fille_contrainte in bobines_fille:
        if not is_valid_bobine_fille_for_bobine_fille(bobine_fille, bobine_fille_contrainte):
            return False
        if bobine_fille.code == bobine_fille_contrainte.code and not bobine_fille_is_neutre(bobine_fille):
            poses.remove(bobine_fille_contrainte.pose)
    if poses:
        return True
    return False


def is_valid_bobine_fille_for_bobine_fille(bobines_fille, bobine_fille_contrainte):
    if bobines_fille.color != bobine_fille_contrainte.color:
        return False
    if bobines_fille.gr != bobine_fille_contrainte.gr:
        return False
    if bobines_fille.lenght != bobine_fille_contrainte.lenght:
        return False
    return True


def bobine_fille_is_neutre(bobine_fille):
    for pose in bobine_fille.poses:
        if pose == 0:
            return True
        return False


# FILTRE BOBINE POLY


def filter_bobines_poly_for_bobines_papier(bobines_poly, bobines_papier):
    new_bobine_poly = []
    for bobine_poly in bobines_poly:
        if is_valid_bobine_poly_for_bobines_papier(bobine_poly, bobines_papier):
            new_bobine_poly.append(bobine_poly)
    return new_bobine_poly


def is_valid_bobine_poly_for_bobines_papier(bobine_poly, bobines_papier):
    for bobine_papier in bobines_papier:
        if bobine_poly.laize == bobine_papier.laize:
            return True
    return False


# FILTRE PERFO


def filter_perfos_for_refentes(perfos, refentes):
    new_perfos = []
    for perfo in perfos:
        if is_valid_perfo_for_refentes(perfo, refentes):
            new_perfos.append(perfo)
    return new_perfos


def is_valid_perfo_for_refentes(perfo, refentes):
    for refente in refentes:
        if perfo.code == refente.code_perfo:
            return True
    return False
