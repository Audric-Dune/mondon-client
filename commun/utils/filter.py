# !/usr/bin/env python
# -*- coding: utf-8 -*-

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


def filter_refentes_for_bobines_fille(refentes, bobines_fille):
    new_refentes = []
    for refente in refentes:
        if is_valid_refente_for_bobines_fille(refente, bobines_fille):
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
    if not is_valid_refente_for_bobines_fille(refente, bobines_fille=contrainte.bobines_fille):
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


def is_valid_refente_for_bobines_fille(refente, bobines_fille):
    return True


# FILTRE BOBINES FILLE


def filter_bobines_fille_for_contrainte(bobines_fille, contrainte):
    new_bobines_fille = []
    for bobine_fille in bobines_fille:
        if is_valid_bobine_fille_for_contrainte(bobine_fille, contrainte):
            new_bobines_fille.append(bobine_fille)
    return new_bobines_fille


def is_valid_bobine_fille_for_contrainte(bobine_fille, contrainte):
    if not is_valid_bobine_fille_for_bobine_papier(bobine_fille, bobine_papier=contrainte.bobine_papier):
        return False
    if not is_valid_bobine_fille_for_refente(bobine_fille, refente=contrainte.refente):
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


def is_valid_bobine_fille_for_refente(bobine_fille, refente):
    if not refente:
        return True
    count_pose = 0
    for laize in refente.laizes:
        if bobine_fille.laize == laize:
            count_pose += 1
            for pose in bobine_fille.poses:
                if pose == 0:
                    return True
                if pose == count_pose:
                    return True
    return False


def is_valid_bobine_fille_for_bobines_fille(bobine_fille, bobines_fille):
    if not bobines_fille:
        return True
    # Bobine_fille:
    # poses = [listes des poses disponible]; exemple: [1,2,4]
    # pose = pose sélectionnée dans la list des poses; exemple: 2
    poses = bobine_fille.poses
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
